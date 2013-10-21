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
pbar = ProgressBar(widgets=widgets, maxval=len(NYCzips))
pbar.start()

for indexz, zipcode in enumerate(NYCzips):

	exec("inFile=open('%s','r')" % (str(zipcode)+'results2woClosed'))
	locations = pickle.load(inFile)
	inFile.close()	



	for index,location in enumerate(locations):
		pbar.update(indexz+1)
		countTotal+=1
	
pbar.finish()
print str(countTotal)+' total restaurants in data set'

