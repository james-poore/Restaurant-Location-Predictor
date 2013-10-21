import pickle
from bs4 import BeautifulSoup
from specialFunctions2 import NYCzips, CGRestaurant,crossCheck
import time


for zipcode in NYCzips[:11]:
    matchCount = 0
    matchIndex = -1
    goodList = []

    exec("cgFile=open('%s','r')" % (str(zipcode)+'results2woClosed'))
    exec("yelpedFile=open('%s','r')" % (str(zipcode)+'results2Yelped'))
    
    cgLocations = pickle.load(cgFile)
    yelpedLocations = pickle.load(yelpedFile)
    cgFile.close()
    yelpedFile.close()

    for location in yelpedLocations:
        for index, cgLocation in enumerate(cgLocations):
            cgSoup = BeautifulSoup(cgLocation,'xml')
            cgRest = CGRestaurant(cgSoup)
            cgRest.fix_types
            if crossCheck(location[0],cgRest.name,'name'):
                matchCount+=1
                matchIndex = index
        if matchCount > 1:
            print "Too many matches for " + location[0]
            continue
        elif matchIndex < 0:
            print "No matches found for " + location[0]
        else:
            print "Only 1 match found, fixing..."
            location[3] = ((location[3]/(cgRest.reviewCount+abs(location[4]-cgRest.reviewCount)))-(cgRest.rating*cgRest.reviewCount))/abs(location[4]-cg.reviewCount)
            goodList = []
            
    if len(goodList) == len(yelpedLocations):
        print 'All good in ' + str(zipcode)
        exec("output=open('%s','w')" % (str(zipcode)+'results2Yelpedclean'))
        pickle.dump(goodList,output)
    else:
        print 'Duplicates found in %d, :('


            
        
