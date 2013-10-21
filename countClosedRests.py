import pickle
from bs4 import BeautifulSoup
import sys
from progressbar import *
import time
from specialFunctions import NYCzips,getPercentDiff

countTotal = 0
souper = BeautifulSoup('html')
widgets = ['Running: ', Percentage(), ' ',
		   Bar(marker='0',left='[',right=']'),
		   ' ', ETA()]

for indexz, zipcode in enumerate(NYCzips):
	goodlist = []
	thisCount = 0
	exec("inFile=open('%s','r')" % (str(zipcode)+'results2'))
	exec("outFile=open('%s','w')" % (str(zipcode)+'results2woClosed'))
	locations = pickle.load(inFile)
	inFile.close()	

	pbar = ProgressBar(widgets=widgets, maxval=len(NYCzips))
	pbar.start()

	for index,location in enumerate(locations):
		pbar.update(indexz+1)
		soup = BeautifulSoup(location,'xml')
		if soup.business_operation_status.string == unicode(0):
			thisCount+=1
		else:
			goodlist.append(location)
	print str(thisCount)+' restaurants closed in zip: '+str(zipcode)
	countTotal+=thisCount
	pickle.dump(goodlist,outFile)
	del goodlist
	outFile.close()
	
pbar.finish()
print str(countTotal)+' total restaurants closed in data set'

