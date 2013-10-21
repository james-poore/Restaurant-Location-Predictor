import pickle
import sys
import time
import traceback
from urllib2 import urlopen
from bs4 import BeautifulSoup
from progressbar import *
from specialFunctions import NYCzips, getTags, getPercentDiff,YelpRestaurant,CGRestaurant,getYelpURL2, findRestMatch


verbose = False
zipContinue = False
indexContinue = False

programfail=False

try:
	if sys.argv[1] == '--verbose':
		verbose = True
	if int(sys.argv[2]):
		zipContinue = sys.argv[2]
	if int(sys.argv[3]):
		indexContinue = sys.argv[3]
except:
	pass

def ratingRound(numstr):
	last = int(numstr[-1])
	if last < 3:
		return float(numstr[:2]+str(0))
	elif last < 8:
		return float(numstr[:2]+str(5))
	else:
		last = 0
		return float(str(float(numstr)+1.0)[:2]+str(0))

outFile = type(file)
goodlist = [[0,0]]

def sighandler(signal,frame):
	if programfail:
		print "Code fail"
	else:
		print "Ctrl+C pressed: storing Yelp data"
	pickle.dump(goodlist,outFile)
	print 'Program halted at ZIP: %d; INDEX: %d' % (goodlist[0][0],goodlist[0][1])
	outFile.close()
	print 'Everything pickled and saved! YAY!'
	sys.exit(1)
	exit(-1)

uncatchable = ['SIG_DFL','SIGSTOP','SIGKILL']
for i in [x for x in dir(signal) if x.startswith("SIG")]:
	if not i in uncatchable:
                signum = getattr(signal,i)
                signal.signal(signum,sighandler)

checked = 0
failPriceCount = 0
failReviewCount = 0
totalGoodCount = 0
zipRestCount = {}
failBoth = 0
failNoMatch = 0
bothTest = 0
souper = BeautifulSoup('html')
widgets = ['Running: ', Percentage(), ' ',
		   Bar(marker='0',left='[',right=']'),
		   ' ', Timer()]

pbar = ProgressBar(widgets=widgets, maxval=len(NYCzips))
pbar.start()
try:
	for indexz,zipcode in enumerate(NYCzips[:11]):
	#if zipcode < zipContinue:
		#continue
		print 'Zip: %d ==============================================================================' % (zipcode)
		goodcount = 0
		locStart = 0
		goodlist = [[zipcode,0]]
		zipRestCount[zipcode] = 0
		try:
			exec("restartFile=open('%s','r')" % (str(zipcode)+'results2Yelped'))
			print 'Found a Yelp! results file for %d. Checking to see if we need to continue...' % (zipcode)
			checkpoint = pickle.load(restartFile)
			restartFile.close()
			if checkpoint[0][0] == zipcode:
				locStart = checkpoint[0][1]
				print 'Yep. We need to continue from index ' + str(locStart)
				goodlist = checkpoint
				checked+=locStart
				totalGoodCount+=len(checkpoint[1:])
				zipRestCount+=len(checkpoint[1:])
			else:
				print 'Nope. This file looks complete. Moving on...'
				exec("inFile=open('%s','r')" % (str(zipcode)+'results2woClosed'))
				checked+=len(pickle.load(inFile))
				totalGoodCount+=len(checkpoint)
				zipRestCount[zipcode] = len(checkpoint)
				inFile.close()
				continue
		except:
			pass
		exec("inFile=open('%s','r')" % (str(zipcode)+'results2woClosed'))
		exec("outFile=open('%s','w')" % (str(zipcode)+'results2Yelped'))
		locations = pickle.load(inFile)
		inFile.close()	

		for index,location in enumerate(locations[locStart:]):
		#if (zipcode == zipContinue and index < indexContinue):
			#continue
			index = index + locStart
			goodlist[0][1] = index
			pbar.update(indexz+1)
			
			soup = BeautifulSoup(location,'xml')
			cgRest = CGRestaurant(soup)
			print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' Yelp Page Grab'
			try:
				yelpSoup = BeautifulSoup(urlopen(getYelpURL2(cgRest.name,cgRest.zip)))
			except:
				yelpSoup = BeautifulSoup(urlopen(getYelpURL2(cgRest.name,cgRest.zip)))
			time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' Yelp Page Grab'
			yelpRest = findRestMatch(cgRest, yelpSoup,checked,totalGoodCount,index)
		#Look at next page for more hits if not finding enough matches
			cgRest.fix_types()
			if yelpRest:
				if verbose:
					print '\n\n\n!!!!!!!!!!!!'
					print 'MATCH FOUND'
					print '!!!!!!!!!!!!'
					print '(((((((((( ' + str([cgRest.desc]) + ':::' + str([yelpRest.desc]) + ' ))))))))))'
				yelpRest.fix_types()
				if yelpRest.name:
					cgRest.name = yelpRest.name
				cgRest.categoryTags = cgRest.categoryTags + yelpRest.categoryTags
			
			#check if yelpRest has rating, user_review_count, and price data
				if yelpRest.price in ['$','$$','$$$','$$$$'] and yelpRest.rating: ###yelp restaurant has price and rating data
					print 'IIIIIIIIIIIIIIIIIII YELP HAS PRICE IIIIIIIIIIIIIIIIIIIII'
					if cgRest.price in ['$','$$','$$$','$$$$'] and cgRest.rating: 
						cgRest.rating = ( (cgRest.rating*float(cgRest.reviewCount))+(yelpRest.rating*float(yelpRest.reviewCount))) / (float(cgRest.reviewCount)+float(yelpRest.reviewCount))
						cgRest.rating = ratingRound('{0:.1f}'.format(cgRest.rating))
						cgRest.reviewCount = cgRest.reviewCount + yelpRest.reviewCount
					elif (not cgRest.price in ['$','$$','$$$','$$$$']) and (not cgRest.rating):
						cgRest.price = yelpRest.price
						cgRest.rating = yelpRest.rating
						cgRest.reviewCount = yelpRest.reviewCount
					elif (not cgRest.price in ['$','$$','$$$','$$$$']):
						cgRest.price = yelpRest.price
						cgRest.rating = ( (cgRest.rating*float(cgRest.reviewCount))+(yelpRest.rating*float(yelpRest.reviewCount))) / (float(cgRest.reviewCount)+float(yelpRest.reviewCount))
						cgRest.rating = ratingRound('{0:.1f}'.format(cgRest.rating))
						cgRest.reviewCount = cgRest.reviewCount + yelpRest.reviewCount
					else:
						cgRest.rating = yelpRest.rating
						cgRest.reviewCount = yelpRest.reviewCount

				elif yelpRest.rating: ###yelp restaurant is missing price data, has rating data
					print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII YELP DOESNT HAVE PRICE'
					if cgRest.price in ['$','$$','$$$','$$$$'] and cgRest.rating:
						cgRest.rating = ( (cgRest.rating*float(cgRest.reviewCount))+(yelpRest.rating*float(yelpRest.reviewCount))) / (float(cgRest.reviewCount)+float(yelpRest.reviewCount))
						cgRest.rating = ratingRound('{0:.1f}'.format(cgRest.rating))
						cgRest.reviewCount = cgRest.reviewCount + yelpRest.reviewCount
					elif cgRest.price in ['$','$$','$$$','$$$$']:
						cgRest.rating = yelpRest.rating
						cgRest.reviewCount = yelpRest.reviewCount
					else:
						print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX NEITHER CG OR YELP HAS PRICE DATA'

			if cgRest.price in ['$','$$','$$$','$$$$'] and cgRest.rating and cgRest.reviewCount >= 10 and cgRest.zip: #if restaurant
				goodlist.append(cgRest.useful_data())
				zipRestCount[zipcode]+=1
				goodcount+=1
				totalGoodCount+=1
				if verbose:
					print '++++++++++++++PASS!:::::::::Running Count = ' + str(totalGoodCount) + '; Price: ' + str(cgRest.price) +', Rating: ' + str(cgRest.rating) + ', Rev Count: ' + str(cgRest.reviewCount)
			try:
				if (not cgRest.price in ['$','$$','$$$','$$$$']):
					failPriceCount+=1
					if verbose:
						try:
							print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   FAIL, MISSING PRICE:::::::::Running Count = ' + str(failPriceCount) + '   price: ' + cgRest.price  + '    ' + str(cgRest.desc)
						except:
							print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   FAIL, MISSING PRICE:::::::::Running Count = ' + str(failPriceCount) + '    ' + str(cgRest.desc)
						
			except Exception, e:
				print "[-] Error = "+str(e)
				print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     FAILED PRICE CHECK FAIL COUNT: price---> ' + cgRest.price
				failPriceCount+=1
				if verbose:
					print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   FAIL, MISSING PRICE:::::::::Running Count = ' + str(failPriceCount) + '    ' + str(cgRest.desc)
				
			try:
				if (not cgRest.rating) or cgRest.reviewCount < 10:
					try:
						print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   ' + str(cgRest.rating) + ' ' + str(cgRest.reviewCount) + ' ' + str(yelpRest.rating) + ' ' + str(yelpRest.reviewCount) + ' RATING OR REVIEW COUNT FAIL'+ str(cgRest.desc)
					except:
						print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   ' + str(cgRest.rating) + ' ' + str(cgRest.reviewCount) + ' ' + '   RATING OR REVIEW COUNT FAIL'  + '    ' + str(cgRest.desc)
					failReviewCount+=1
					if verbose:
						print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   FAIL on LOW REVIEWS: Review Count = '+ str(cgRest.reviewCount) + '   ::::::Running Count = ' + str(failReviewCount)  + '    ' + str(cgRest.desc)
				if bothTest != failPriceCount:
					failBoth+=1
			except Exception, e:
				print "[-] Error = "+str(e)
				print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    FAILED LOW REVIEW FAIL COUNT: ---> rating: ' + str(cgRest.rating) + ', reviewCount: ' + str(cgRest.reviewCount)  + '    ' + str(cgRest.desc)
				failReviewCount+=1
				if verbose:
					print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   FAIL on LOW REVIEWS: Review Count = '+ str(cgRest.reviewCount) + '   ::::::Running Count = ' + str(failReviewCount)  + '    ' + str(cgRest.desc)
				if bothTest != failPriceCount:
					failBoth+=1

			bothTest = failPriceCount
			goodlist[0][1]+=1
			checked+=1
			
			del cgRest
			del yelpRest
		print 'ZIP SUMMARY:'
		print '---------------------------------'
		print '%d restaurants checked in zip, total checked: %d' % (goodlist[0][1]-1,checked)
		print '%d restaurants passed' % (totalGoodCount)
		print '%d total failed' % (goodlist[0][1]-goodcount) 
		print '%d restaurants failed for not having a price' % abs(failPriceCount-failBoth)
		print '%d restaurants failed for not having enough reviews (10 or more)' % abs(failReviewCount-failBoth)
		print '%d restaurants failed for not having a price or enough reviews' % (failBoth)
		print '======================================================================================================================'
	
		goodlist.pop(0)
		print goodlist
		print '======================================================================================================================\n'
		pickle.dump(goodlist,outFile)
		outFile.close()
		del goodlist
except Exception, e:
	print "[-] Error = "+str(e)
	exc_type, exc_value, exc_traceback = sys.exc_info()
	print "*** print_tb:"
	traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
	print "*** print_exception:"
	traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)
	print "*** print_exc:"
	traceback.print_exc()
	print "*** format_exc, first and last line:"
	formatted_lines = traceback.format_exc().splitlines()
	print formatted_lines[0]
	print formatted_lines[-1]
	print "*** format_exception:"
	print repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	print "*** extract_tb:"
	print repr(traceback.extract_tb(exc_traceback))
	print "*** format_tb:"
	print repr(traceback.format_tb(exc_traceback))
	print "*** tb_lineno:", exc_traceback.tb_lineno
	print '==============================================='
	print '         Finished. Printing Summary'
	for zipcode in zipRestCount:
		print str(zipcode) + ':\t' + str(zipRestCount[zipcode])
	print '==============================================='
	print 'Total: %d' % (totalGoodCount)	
	sighandler('signal','frame')

try: 
	pbar.finish()
except:
	pass

print '==============================================='
print '         Finished. Printing Summary'
for zipcode in zipRestCount:
	print str(zipcode) + ':\t' + str(zipRestCount[zipcode])
print '==============================================='
print 'Total: %d' % (totalGoodCount)
















