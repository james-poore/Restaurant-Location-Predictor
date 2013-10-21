import pickle
from bs4 import BeautifulSoup
import sys
from progressbar import *
import time
from specialFunctions import NYCzips,getPercentDiff

def crossCheck(thisone, thatone):
		err = [thisone,thatone]
		for word in ['&',' AND ',' ST. ',' ST ',' STREET ',' AVE ',' AVE. ',' AVENUE ','@']:
					thisone[1] = thisone[1].replace(word,'')
					thatone[1] = thatone[1].replace(word,'')
		thisAddNum = thisone[1].split(' ')[0]
		thatAddNum = thatone[1].split(' ')[0]
		if getPercentDiff(thisone[1], thatone[1]) >= 0.69 and thisone[2] == thatone[2] and thisone[3] == thatone[3]:
			if thisAddNum.isdigit() and thatAddNum.isdigit() and abs(int(thisAddNum) - int(thatAddNum)) < 10:			
				return True
			else:
				return False
		else:
			return False
			
dupCount = 0
restDict = {}



for indexz, zipcode in enumerate(NYCzips):
	restDict[zipcode] = {}
	
	checkList = []
	while 1:	
		try:	
			exec("file=open('%s','r')" % (str(zipcode)+sys.argv[1]))
			break
		except:
			filename = raw_input('Enter the correct filetype: ')

	locations = pickle.load(file)
	limit = len(locations)+1
	file.close()
	p = ProgressBar(widgets=[str((float(indexz+1)/float(len(NYCzips)))*100)[:4]+'% through zips: ',Percentage(),Bar(),Timer()],maxval=limit)
	p.start()
	for index, location in enumerate(locations):
		checkPass = True
		p.update(index+1)
		soup = BeautifulSoup(location,'xml')
		restName = soup.find_all('name')[0].string.upper()
		restAddress = soup.street.string.upper()
		restPhone = soup.phone_number.string
		check = [index,restAddress,zipcode,restPhone]
		
		if restName in restDict[zipcode]:
			#print restName + '  ' + str(restDict[zipcode][restName])
			#time.sleep(0.75)
			restDict[zipcode][restName][0]+=1
			for item in restDict[zipcode][restName][1]:
				if crossCheck(check,item):
					print restName + '=====' + str(check[1:]) + ' : ' + str(item[1:])
					dupCount+=1
					checkPass = False
					break
			if checkPass:
				restDict[zipcode][restName][1].append([index,restAddress,zipcode,restPhone])
				
		else:
			restDict[zipcode][restName] = [1,[[index,restAddress,zipcode,restPhone]]]
	p.finish()

print str(dupCount) + ' total duplicates'
