import pickle
import urllib2
import json
import signal
import sys
from bs4 import BeautifulSoup
from progressbar import ProgressBar,Percentage,Bar,Timer,ETA
from specialFunctions import NYCzips, getYelpURL, getPercentDiff,yelp,getTags


try:
	file = open('YelpTags','r') #dictionary containing tags found in Yelp API calls, ADD A FREQUENCY COUNT FOR SORTING IN THE FUTURE
	yelpTags = pickle.load(file)
	file.close()
except:
	yelpTags = {}
try:
	file = open('YelpChecks','r') #a dictionary of zipcodes with corresponding completion status and restaurants requiring checks
	yelpChecks = pickle.load(file)
	file.close()
except:
	yelpChecks = {} 
try:
	file = open('YelpResults','r')
	yelpResults = pickle.load(file)
	file.close()
except:
	yelpResults = []
	

outFile = file
newlist = []

yelpTagsFile = open('YelpTags','w')
yelpChecksFile = open('YelpChecks','w')
yelpResultsFile = open('YelpResults','w')

def sighandler(signal,frame):
	print "Ctrl+C pressed or ERROR: storing Yelp data"
	print Exception
	pickle.dump(yelpTags, yelpTagsFile)
	pickle.dump(yelpChecks, yelpChecksFile)
	pickle.dump(yelpResults, yelpResultsFile)
	pickle.dump(newlist,outFile)
	yelpTagsFile.close()
	yelpChecksFile.close()
	sys.exit(1)
	exit(-1)

uncatchable = ['SIG_DFL','SIGSTOP','SIGKILL']
for i in [x for x in dir(signal) if x.startswith("SIG")]:
	if not i in uncatchable:
                signum = getattr(signal,i)
                signal.signal(signum,sighandler)

souper = BeautifulSoup('html')

yelpedCountTotal = 0
flagged = 0
badLoc = 0
badSearch = 0
yelpFinds = []

for zipcode in NYCzips[1:]: ############################# ADD CHECK FOR ZIPCODE FROM YELPCHECK AS WELL AS INDEX FOR CONTINUATION POINT, FIX STORAGE

	widgets = [str(zipcode)+': ', Percentage(), ' ',
		   Bar(marker='0',left='[',right=']'),
		   ' ', ETA()]

	try:
		if yelpCheck[zipcode]:
			print 'Found ' + str(zipcode) + ' in YelpChecks'
			continue
	except:
		yelpChecks[zipcode]=['started']
	
	newlist=[]
	try:
		exec("yelped=open('%s','r')" % (str(zipcode)+'results2yelped'))
		newlist = pickle.load(yelped)
		yelped.close()
	except:
		pass

	yelpedCount = 0
	exec("inFile=open('%s','r')" % (str(zipcode)+'results2'))
	exec("outFile=open('%s','w')" % (str(zipcode)+'results2yelped'))
	locations = pickle.load(inFile)
	inFile.close()	

	pbar = ProgressBar(widgets=widgets, maxval=len(locations))
	pbar.start()

	for index,location in enumerate(locations):

		pbar.update(index+1)

		if yelpChecks[zipcode][0] != 'started' and index <= yelpChecks[zipcode][0]:
			print yelpChecks[zipcode] 
			print '@ Location Continue'
			continue
		else:
			soup = BeautifulSoup(location,'xml')
			cgRestName = soup.find_all('name')[0].string
			cgLat = soup.latitude.string
			cgLon = soup.longitude.string
			cityRevCount = int(soup.user_review_count.text)
			
			if cityRevCount < 8:
				print '\n===========Next Check===========[[[%s :: %s]]]' % (zipcode,index)
				print "Old Review Count = " + soup.user_review_count.text
				yelpURL = getYelpURL(cgRestName,cgLat,cgLon).encode('ascii','ignore')
				yelpData = json.load(urllib2.urlopen(yelpURL))
				#print str(yelpData)[:100]

				if len(yelpData['businesses']) > 0:
					yelpRevCount = yelp(yelpData,'review_count')
					cgAddress = unicode(soup.street.string)
					cgPhone = unicode(soup.phone_number.string)
					yelpRestName = unicode(yelp(yelpData,'name'))
					yelpAddress = unicode(yelp(yelpData,'address1'))
					yelpPhone = unicode(yelp(yelpData,'phone'))
					yelpLat = unicode(yelp(yelpData,'latitude'))
					yelpLon = unicode(yelp(yelpData,'longitude'))
					info = [['CityGrid',cgRestName,cgAddress,cgPhone,cgLat,cgLon],['Yelp',yelpRestName,yelpAddress,yelpPhone,yelpLat,yelpLon]]
					try:
						print cgAddress + '   ' + yelpAddress + '   ' + str(getPercentDiff(cgAddress.upper(),yelpAddress.upper()))
					except:
						pass
					try:
						print cgRestName + '   ' + yelpRestName  + '   ' + str(getPercentDiff(cgRestName.upper(),yelpRestName.upper()))
					except:
						pass
					try:
						print cgPhone + '   ' + yelpPhone
					except:
						pass
					
					if getPercentDiff(cgAddress.upper(),yelpAddress.upper()) >= 0.6 or (cgPhone == yelpPhone and yelpLat[:8] == cgLat[:8] and yelpLon[:9] == cgLon[:9]):
						if getPercentDiff(cgRestName.upper(),yelpRestName.upper()) >= 0.6:
							#soup.location.name = 'YELPED' #when yelp values added location id changed to YELPED		
							#soup.user_review_count.string = str(cityRevCount + yelpRevCount)
							soup.location.append(souper.new_tag('yelped_review_count'))
							soup.location.yelped_review_count.append(unicode(cityRevCount + yelpRevCount))
							print "New Review Count = " + str(soup.yelped_review_count.text)
							print "Old Rating = " + soup.rating.text + " Yelp Rating = " + str(yelp(yelpData,'avg_rating'))
							for tag in yelp(yelpData,'categories'):
								try:
									yelpTags[tag['name']]
								
								except:
									yelpTags[tag['name']]=len(yelpTags)+1
								if tag['name'] not in getTags(soup):
									soup.tags.append(souper.new_tag('tag',id='yelp'+str(yelpTags[tag['name']])))
									soup.tags.contents[-1].append(tag['name'])
							try: 
								newRating = unicode( (float(soup.rating.string)*cityRevCount + float(yelp(yelpData,'avg_rating')*2*yelpRevCount))/float(yelpRevCount + cityRevCount))
								soup.location.append(souper.new_tag('yelped_rating'))
								soup.location.yelped_rating.append(newRating)
								
							except:
								soup.location.append(souper.new_tag('yelped_rating'))
								soup.location.yelped_rating.append(str(float(yelp(yelpData,'avg_rating'))*2))
							print "New Rating = " + soup.yelped_rating.string
							yelpedCount+=1
						else:
							yelpResults.append(str(yelpData))
							print 'FLAGGED: ' + cgRestName + '   ' + yelp(yelpData,'name') + ' ::: ' + str(getPercentDiff(cgRestName,yelp(yelpData,'name')))
							yelpChecks[zipcode].append([index,'FLAGGED: ' + cgRestName + ' ' + yelpRestName + ' ::: ' + str(getPercentDiff(cgRestName,yelpRestName)),info])
							flagged+=1
					else:
						yelpResults.append(str(yelpData))
						print 'LOCATION MISMATCH: ' + cgRestName + '   ' + yelp(yelpData,'name') + '   ' + str(getPercentDiff(cgAddress.upper(),yelpAddress.upper()))
						yelpChecks[zipcode].append([index,'LOCATION MISMATCH: ' + cgRestName + ', ' + cgAddress + ' :: ' + yelpAddress + ' :: ' + str(getPercentDiff(cgAddress.upper(),yelpAddress.upper())),info])
						badLoc+=1
				else:
					yelpResults.append(str(yelpData))
					print 'BAD SEARCH: RETURNED NOTHING'
					yelpChecks[zipcode].append([index,'BAD SEARCH: RETURNED NOTHING',info])
					badSearch+=1
		
		newlist.append(str(soup))
		yelpChecks[zipcode][0] = index
		pbar.finish()
	pickle.dump(newlist,outFile)
	#yelpTagsFile.close()
	#yelpChecksFile.close()
	yelpedCountTotal+=yelpedCount
	print str(yelpedCount) + " locations yelped in " + str(zipcode) + ", " + str(yelpedCountTotal) + " total"									  
	print 'flagged: ' + str(flagged) + '; badSearch: ' + str(badSearch) + '; badLoc: ' + str(badLoc)
	outFile.close()

pickle.dump(yelpTags, yelpTagsFile)
pickle.dump(yelpChecks, yelpChecksFile)
pickle.dump(yelpResults, yelpResultsFile)
print str(yelpedCountTotal) + " locations yelped overall"
