import pickle
import sys
from specialFunctions import testZip, testReviewCount, checkTags,NYCzips
from bs4 import BeautifulSoup
from progressbar import ProgressBar, Percentage,Bar,Timer

revThreshold = int(sys.argv[1])

remCount = 0
restCount = 0
badZipCount = 0
badReviewCount = 0
badTagCount = 0

p = ProgressBar(widgets=[Percentage(),Bar(),Timer()], maxval=len(NYCzips))
p.start()

for index,zipcode in enumerate(NYCzips):
	lowlist = []
	exec("picklefile = open('%s','r')" % (str(zipcode) + 'results2'))
	exec("output = open('%s','w')" % (str(zipcode)+'reviewslt'+str(revThreshold)))
	locationListstrings = pickle.load(picklefile)
	picklefile.close()
	for location in locationListstrings:
		soup = BeautifulSoup(location,'xml')
		if not testReviewCount(soup,revThreshold):
			#print soup.user_review_count.text
			badReviewCount+=1
			lowlist.append(location)

	pickle.dump(lowlist,output)
	remCount+=len(lowlist)
	restCount+=len(locationListstrings)
	print str(len(lowlist)) + ' locations removed for zip: ' + str(zipcode)
	output.close()
	p.update(index+1)
p.finish()
print "Restaurants with # of reviews < " + str(revThreshold) + ": " + str(remCount)
print str(restCount-remCount) + ' restaurants are ok'
