import pickle
from bs4 import BeautifulSoup
from progressbar import ProgressBar, Percentage,Bar,Timer
from specialFunctions import NYCzips, getTags


locationsTotal = 0
oneTaggerCount = 0

zipcount = len(NYCzips)
p = ProgressBar(widgets=[Percentage(),Bar(),Timer()], maxval=zipcount)
p.start()

for index, zipcode in enumerate(NYCzips):
	exec("data = open('%s','r')" % (str(zipcode)+'results2'))
	locations = pickle.load(data)
	locationsTotal+=len(locations)
	for location in locations:
		soup = BeautifulSoup(location,'xml')
		tags = getTags(soup)
		if len(tags) == 1:
			oneTaggerCount+=1
	
	p.update(index+1)

p.finish()
print str((float(oneTaggerCount)/float(locationsTotal))*100)[:4] + '% of locations have only one tag :('
print str(oneTaggerCount) + ' out of ' + str(locationsTotal)
