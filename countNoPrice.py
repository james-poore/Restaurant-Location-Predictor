import pickle
from specialFunctions import NYCzips,getTags
from bs4 import BeautifulSoup
from progressbar import ProgressBar, Percentage,Bar,Timer

prices = ['$','$$','$$$','$$$$']

locationsTotal = 0
havePriceCount = 0

zipcount = len(NYCzips)

p = ProgressBar(widgets=[Percentage(),Bar(),Timer()], maxval=zipcount)
p.start()

for index,zipcode in enumerate(NYCzips):
	exec("data = open('%s','r')" % (str(zipcode)+'results2'))
	locations = pickle.load(data)
	locationsTotal+=len(locations)
	for location in locations:
		soup = BeautifulSoup(location,'xml')
		tags = getTags(soup)
		for price in prices:
			if price in tags:
				havePriceCount+=1
				break
	p.update(index+1)
p.finish()
print str((float(havePriceCount)/float(locationsTotal))*100)[:4] + '% of locations have price info'
print str(havePriceCount) + ' out of ' + str(locationsTotal)
				
