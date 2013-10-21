from bs4 import BeautifulSoup
from urllib2 import urlopen
import oauth2

class YelpRestaurant:
	def __init__(self, bizSoup): ############################# DEFINITELY CHECK TO MAKE SURE BUSINESS IS NOT CLOSED DOWN
		self.soup = bizSoup
		self.link = 'http://www.yelp.com'+bizSoup.h4.a['href']
		self.pageSoup = BeautifulSoup(urlopen(self.link))
				
		self.name = bizSoup.h4.a.text[bizSoup.h4.a.text.find('\t')+1:bizSoup.h4.a.text.find('\n')]
		print '\n@@@@@@@@@@@@@@@@@@@@ YELP NAME: ' + self.name
		self.address = bizSoup.address.div.prettify().replace('\n','').replace('<br>','').replace('<br >','').split('<br/>')[0][6:-1]
		if self.address.split(' ')[0].isdigit():
			self.city = bizSoup.address.div.prettify().replace('\n','').replace('<br>','').replace('<br >','').split('<br/>')[1].split(',')[0][1:]
			self.state = bizSoup.address.div.prettify().replace('\n','').replace('<br>','').replace('<br >','').split('<br/>')[1].split(',')[0][1:]
		else:
			self.city = ''
			self.state = ''
		try:
			self.zip = bizSoup.address.div.prettify().replace('\n','').replace('<br>','').replace('<br >','').split('<br/>')[1].split(',')[1].split(' ')[2][:-6]
		except:
			self.zip = 0
		self.lat = self.pageSoup.find('meta',{'property':'place:location:latitude'})['content']
		self.lon = self.pageSoup.find('meta',{'property':'place:location:longitude'})['content']
		try:
			self.phone = self.pageSoup.find('span',{'id':'bizPhone'}).string.replace('(','').replace(')','').replace(' ','').replace('-','')
		except:
			self.phone = ''
		try:
			self.rating = self.pageSoup.find('meta',{'itemprop':'ratingValue'})['content']
			print '****************************** Yelp rating      |' + str(self.rating)
		except Exception, e:
			print "****************************** Yelp rating fail in object creation [-] Error = "+str(e)
			#print "    YELP RATING set to: " + str(self.rating)
			self.rating = 0
		try:
			self.reviewCount = self.pageSoup.find('span',{'itemprop':'reviewCount'}).string
		except:
			self.reviewCount = 0
		print '****************************** Yelp review count = ' + str(self.reviewCount)
		self.categoryTags = [x.string.replace('\n','').replace('\t','') for x in self.pageSoup.find('span',{'id':'cat_display'}).find_all('a')]
		try:
			self.price = self.pageSoup.find('span',{'id':'price_tip'}).string
			print '****************************** Yelp price     |' + str(self.price)
		except Exception, e:
			print "****************************** Yelp price fail in object creation [-] Error = "+str(e)
			#print "    YELP PRICE set to: " + str(self.price)
			self.price = ''                                                ########################### CHECK IF PRICE IS ZERO REPLACE WITH CG PRICE IF POSSIBLE
		self.desc = [self.name,self.address,self.zip,self.phone]
		
	def fix_types(self):
		self.name = unicode(self.name)
		try:
			self.address = unicode(self.address)
		except:
			self.address = ''
		try:
			self.city = unicode(self.city)
		except:
			self.city = ''
		try:
			self.state = unicode(self.state)
		except:
			self.state = ''
		try:
			self.zip = int(self.zip)
		except:
			self.zip = 0
		try:
			self.lat = float(self.lat)
		except:
			self.lat = 0
		try:
			self.lon = float(self.lon)
		except:
			self.lon = 0
		try:
			self.phone = unicode(self.phone)
		except:
			self.phone = ''
		try:
			self.rating = float(self.rating)*2.0
			print '}}}}}}}}}}}}}}}}}}}} Yelp Rating post multi: ' + str(self.rating)
		except Exception, e:
			print "}}}}}}}}}}}}}}}}}}}} Yelp Rating fail in fix_types [-] Error = "+str(e)
			print " YELP RATING in fix_types set to:" + str(self.rating)
			self.rating = 0
		try:
			self.reviewCount = int(self.reviewCount)
		except:
			self.reviewCount = 0
		print '}}}}}}}}}}}}}}}}}}}} Yelp review count = ' + str(self.reviewCount)
		try:
			self.categoryTags = [unicode(x) for x in self.categoryTags]
		except:
			self.categoryTags = []
		try:
			self.price = str(self.price)
		except Exception, e:
			print "}}}}}}}}}}}}}}}}}}}} Yelp price fail in fix_types [-] Error = "+str(e)
			self.price = ''
		print "}}}}}}}}}}}}}}}}}}}} Yelp price: " + self.price	
		self.desc = [self.name,self.address,self.zip,self.phone]

class CGRestaurant:
	def __init__(self, locSoup):
		self.name = unicode(locSoup.find_all('name')[0].string).encode('ascii','ignore')
		self.address = locSoup.street.string
		self.city = locSoup.city.string
		self.state = locSoup.state.string
		self.zip = locSoup.postal_code.string
		self.lat = locSoup.latitude.string
		self.lon = locSoup.longitude.string
		self.phone = locSoup.phone_number.string
		self.rating = locSoup.rating.string
		self.reviewCount = locSoup.user_review_count.string
		self.categoryTags = getTags(locSoup)
		self.sampleCategories = locSoup.sample_categories.string
		self.price = findPrice(self.categoryTags)
		self.desc = [self.name,self.address,self.zip,self.phone]

	def useful_data(self):
		retList = [self.name,self.zip,self.price,self.rating,self.reviewCount,self.categoryTags,self.sampleCategories]
		return retList

	def fix_types(self):
		self.name = unicode(self.name)
		try:
			self.address = unicode(self.address)
		except:
			self.address = ''
		try:
			self.city = unicode(self.city)
		except:
			self.city = ''
		try:
			self.state = unicode(self.state)
		except:
			self.state = ''
		try:
			self.zip = int(self.zip)
		except:
			self.zip = 00000
		try:
			self.lat = float(self.lat)
		except:
			self.lat = 0
		try:
			self.lon = float(self.lon)
		except:
			self.lon = 0
		try:
			self.phone = unicode(self.phone)
		except:
			self.phone = ''
		try:
			self.rating = float(self.rating)
			#print '========================= CG rating      |' + str(self.rating)
		except Exception, e:
			#print "========================= CG rating fail in object creation [-] Error = "+str(e)
			#print "    CG RATING set to: " + str(self.rating)
			self.rating = 0
		try:
			self.reviewCount = int(self.reviewCount)
		except:
			self.reviewCount = 0
		#print '========================= CG review count = ' + str(self.reviewCount)
		try:
			self.categoryTags = [unicode(x) for x in self.categoryTags]
		except:
			self.categoryTags = []
		try:
			self.sampleCategories = self.sampleCategories.split(',')
		except:
			self.sampleCategories = []
		try:
			self.price = str(self.price)
		#	print '=========================  CG price     |' + str(self.price)
		except Exception, e:
		#	print "========================= CG price fail in object creation [-] Error = "+str(e)
			print "    CG price set to: " + str(self.rating)
			self.price = ''
		self.desc = [self.name,self.address,self.zip,self.phone]
		

def findPrice(tagslist):
	for price in ['$','$$','$$$','$$$$']:
		if price in tagslist:
			return unicode(price)
	return ''

def cleanString(string):
	for char in ['&']:
		string = string.replace(char,'')
	string = '+'.join([x for x in string.split(' ') if x != ''])
	return string

def getYelpURL2(name,zip):
	name = cleanString(name)
	return 'http://www.yelp.com/search?find_desc='+name+'&find_loc='+zip+'&rpp=10&sortby=best_match'   #&cflt=restaurants,bars

def getBusinessList(soup):
	ret = soup.find('div',{'id':'businessresults'}).find_all('div',{'class':'businessresult clearfix'})
	if ret:
		return ret
	else:
		False
	
def splitNumsAlphas(word):
	alpha = False
	num = False
	keeptrack = ''
	for char in word:
		if char.isalpha():
			alpha = True
			if num:
				return keeptrack + ' ' + splitNumsAlphas(word.replace(keeptrack, keeptrack+' ').split(' ')[1])
			keeptrack = keeptrack + char
		elif char.isdigit():
			num = True
			if alpha:
				return keeptrack + ' ' + splitNumsAlphas(word.replace(keeptrack, keeptrack+' ').split(' ')[1])
			keeptrack = keeptrack + char
	return word
				
				
def fixWords(phrase1,phrase2):
	retPhrase1 = ''
	retPhrase2 = ''
	
	for word in phrase1:
		retPhrase1 = retPhrase1 + splitNumsAlphas(word)
	for word in phrase2:
		retPhrase2 = retPhrase2 + splitNumsAlphas(word)
	
	retPhrase1 = checkSpelling(retPhrase1)

	return retPhrase1, retPhrase2

def crossCheck(thisAddr, thatAddr,which):
	#err = [thisone,thatone]
	#print thisAddr + ':::::::' + thatAddr
	thisAddr = ' '.join([x for x in thisAddr.upper().split(' ') if x != '']).replace(' WEST',' W').replace(' EAST',' E').replace(' SOUTH',' S').replace(' NORTH',' N')
	thatAddr = ' '.join([x for x in thatAddr.upper().split(' ') if x != '']).replace(' WEST',' W').replace(' EAST',' E').replace(' SOUTH',' S').replace(' NORTH',' N')
	
	for word in ['&','AND','STREET','SUITE','STE','ST','AVENUE','AVE','@','.','INC','COMPANY','CORP','CO','LLC',',','(',')','#',"'",'FL ','`','+','=','PLAZA','PLZ','SQUARE','SQ']:
		thisAddr = thisAddr.replace(word,'')
		thatAddr = thatAddr.replace(word,'')
	thisAddr = thisAddr.replace('-',' ')
	thatAddr = thatAddr.replace('-',' ')
		
	thisAddr = ' '.join([x for x in thisAddr.upper().split(' ') if x != '']).replace(' WEST',' W').replace(' EAST',' E').replace(' SOUTH',' S').replace(' NORTH',' N').replace(' FIRST', ' 1').replace(' SECOND',' 2ND').replace(' THIRD',' 3RD').replace(' FOURTH', ' 4TH').replace(' FIFTH', ' 5TH').replace(' SIXTH',' 6TH').replace(' SEVENTH',' 7TH').replace(' EIGHTH',' 8TH').replace(' NINTH',' 9TH').replace(' TENTH',' 10TH').replace(' ELEVENTH',' 11TH').replace(' TWELVTH',' 12TH').replace(' THIRTEENTH',' 13TH').replace(' FOURTEENTH',' 14TH').replace(' FIFTEENTH',' 15TH').replace(' SIXTEENTH',' 16TH').replace(' SEVENTEENTH',' 17TH').replace(' EIGHTEENTH',' 18TH').replace(' NINETEENTH',' 19TH')
	thatAddr = ' '.join([x for x in thatAddr.upper().split(' ') if x != '']).replace(' WEST',' W').replace(' EAST',' E').replace(' SOUTH',' S').replace(' NORTH',' N').replace(' FIRST', ' 1').replace(' SECOND',' 2ND').replace(' THIRD',' 3RD').replace(' FOURTH', ' 4TH').replace(' FIFTH', ' 5TH').replace(' SIXTH',' 6TH').replace(' SEVENTH',' 7TH').replace(' EIGHTH',' 8TH').replace(' NINTH',' 9TH').replace(' TENTH',' 10TH').replace(' ELEVENTH',' 11TH').replace(' TWELVTH',' 12TH').replace(' THIRTEENTH',' 13TH').replace(' FOURTEENTH',' 14TH').replace(' FIFTEENTH',' 15TH').replace(' SIXTEENTH',' 16TH').replace(' SEVENTEENTH',' 17TH').replace(' EIGHTEENTH',' 18TH').replace(' NINETEENTH',' 19TH')

	if 'OF THE AMERICAS' in thisAddr or 'OF THE AMERICAS' in thatAddr:
		thisAddr = thisAddr.replace('OF THE AMERICAS','6TH')
		thatAddr = thatAddr.replace('OF THE AMERICAS','6TH')
	#print thisAddr + ':::::::' + thatAddr
	
	if getPercentDiff(thisAddr, thatAddr) >= 0.6:
	#	print which
		if which == 'add' and (thisAddr.split(' ')[0].isdigit() and thatAddr.split(' ')[0].isdigit()) and abs(int(thisAddr.split(' ')[0]) - int(thatAddr.split(' ')[0])) < 10:			
			return True
		elif which == 'name':
			return True
		else:
	#		print 'SSSSSSSSSSSS  Street # FAIL  SSSSSSSSSSSS'
			return False
	else:
	#	print which
		if getPercentDiff(thisAddr,thatAddr) > .49 and which == 'addr':
			if which == 'add' and (thisAddr.split(' ')[0].isdigit() and thatAddr.split(' ')[0].isdigit()) and abs(int(thisAddr.split(' ')[0]) - int(thatAddr.split(' ')[0])) < 10:			
				return True
	#		print 'SSSSSSSSSSSS  Street # FAIL  SSSSSSSSSSSS'
	#	elif which == 'name':
	#		print 'NNNNNNNNNNNN  NAME FAIL  NNNNNNNNNNNN'
		return False

def findRestMatch(cgRest,yelpSoup,checked,goodcount,indexloc):
	if checked == 0:
		checked = 1
	print "\n\n\n\n\n\n______________________________Checking %s; Checked: %d, Passed: %d, %f_________________________________" % (cgRest.name, checked, goodcount, float(goodcount)/float(checked))
	bizList = getBusinessList(yelpSoup)
	if bizList:
		for index,bizSoup in enumerate(bizList):
			print '_________________________________________________________________________'
			if index > 4:
				break

			yelpRest = YelpRestaurant(bizSoup)
			if index == 0:
				yelpFail = yelpRest
			
			
			print '    LatDiff=' + str(abs(float(cgRest.lat)-float(yelpRest.lat))) + ' : LonDiff' + str(abs(float(cgRest.lon)-float(yelpRest.lon)))
			print str(cgRest.desc) + ':::' + str(yelpRest.desc)
			if cgRest.zip == yelpRest.zip and (cgRest.phone == yelpRest.phone or crossCheck(cgRest.name,yelpRest.name,'name') or crossCheck(cgRest.name.replace(' ', ''),yelpRest.name.replace(' ',''),'name')) and crossCheck(cgRest.address, yelpRest.address,'add'): # and ((abs(float(cgRest.lat)-float(yelpRest.lat)) < 0.004 and abs(float(cgRest.lon)-float(yelpRest.lon)) < 0.004))
				return yelpRest
			else:
				del yelpRest
		print '\n\n\n______________'
		print 'NO MATCH FOUND' # FOR ' + str(cgRest.desc) + ':::' + str(yelpFail.desc) + ' LatDiff=' + str(abs(float(cgRest.lat)-float(yelpFail.lat))) + ' : LonDiff' + str(abs(float(cgRest.lon)-float(yelpFail.lon)))
		print '^^^^^^^^^^^^^^'
		return False
	else:
		print '\n\n\n__________________'
		print 'NO RESULTS ON YELP'
		print '^^^^^^^^^^^^^^^^^^'
	#del yelpRest
		return False

NYCzips = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11001, 11003, 11004, 11005, 11040, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697]

taglist = ['Restaurants', 'Bagel Shops', 'Barbecue Restaurants', 'Brew Pubs', 'Coffeehouses', 'Delis And Delicatessens', 'Dessert Shops', 'Frozen Yogurt Shops', 'Ice Cream Parlors', 'Soda Fountain Shops', 'Shaved Ice', 'Diners', 'Dinner Theaters', 'Doughnut Shops', 'Juice & Smoothie Shops', 'Sandwich Shops', 'Cafes', 'Grill Restaurants', 'Certified Green Restaurant(R)', 'Afghan', 'Ethiopian', 'Moroccan', 'African', 'New American', 'Traditional American', 'Californian', 'Cuban', 'Jamaican', 'Puerto Rican', 'Caribbean', 'Central European', 'Armenian', 'Eastern European', 'Fast Food', 'Health Food', 'Sushi', 'Japanese', 'Argentinean', 'Brazilian', 'Chilean', 'Colombian', 'Costa Rican', 'Mexican', 'Nicaraguan', 'Peruvian', 'Venezuelan', 'Latin American', 'Lebanese', 'Persian', 'Middle Eastern', 'Austrian', 'Belgian', 'English', 'French', 'German', 'Irish', 'Swiss', 'Northern European', 'Danish', 'Norwegian', 'Swedish', 'Scandinavian', 'Seafood', 'Vegan', 'Vegetarian', '$', '$$', '$$$', '$$$$', 'Asian', 'B.Y.O.B.', 'Bar Menu', 'Bar Scene', 'Breakfast', 'Brunch', 'Buffet', 'Burmese', 'Business Breakfast', 'Business Dining', 'Cajun & Creole', 'Cambodian', 'Carry Out', 'Celeb Hangout', 'Cheap Eats', 'Cheesesteak', "Chef's Table", 'Chinese', 'Chowder', 'Cooking', 'Dancing', 'Date Spot', 'Dim Sum', 'Dine At The Bar', 'Eclectic & International', 'Egyptian', 'Espresso Bar', 'Family Style Dining', 'Family-Friendly Dining', 'Filipino', 'Fine Dining', 'Fireplace', 'Food Delivery', 'Greek', 'Group Dining', 'Hamburgers', 'Sliders', 'Happy Hour', 'Hidden Find', 'Historic Setting', 'Hot Dogs', 'Hotel Restaurants', 'Hungarian', 'Indian', 'Indonesian', 'Italian', 'Korean', 'Kosher', 'Late Night Dining', 'Live Music', 'Local Favorite', 'Luaus', 'Lunch Spot', 'Malaysian', 'Meat-And-Three', 'Mediterranean', 'Non-Smoking', 'Noodle Shop', 'Notable Beer List', 'Notable Chef', 'Notable Wine List', 'Online Reservations', 'Outdoor Dining', 'Pan-Asian & Pacific Rim', 'People Watching', 'Pizza', 'Polish & Czech', 'Polynesian', 'Portuguese', 'Private Parties', 'Private Rooms', 'Prix Fixe Menu', 'Quiet', 'Romantic Dining', 'Russian', 'Smoking Permitted', 'Sommelier', 'Soups', 'Southern', 'Southwestern', 'Spanish', 'Special Occasion Dining', 'Steakhouse', 'Tapas / Small Plates', 'Tea Room', 'Thai', 'Theater District Dining', 'Tibetan', 'Trendy Dining', 'Turkish', 'Upscale Casual Dining', 'Vietnamese', 'View Dining', 'Waterfront Dining', 'Casual Date Spot', 'Dining Discounts', 'Margaritas', 'Asian Fusion', 'Chicken', 'European', 'Australian', 'Bistros', 'Chicken Wings', 'Crab House', 'Falafel', 'Halal', 'Nepalese', 'Pakistani', 'Pre Theater Menu', 'Sidewalk Cafes', 'Rodiz126io', 'Comfort Food', 'Szechuan', 'Organic', 'Green', 'Gastro Pub', 'Fondue', 'Soul', 'South American', 'Cyber Cafes', 'Gluten-Free', 'Food Trucks', 'Food Stands', 'Free Wi-Fi', 'Beer & Wine Only', 'HAWAIIAN', 'Salads', 'Refreshment Stands']

def firstFilterTest(locSoup, zipcode):
	if testReviewCount(locSoup,1) and testZip(locSoup, zipcode) and checkTags(locSoup):
		return True
	else:
		return False

def checkTags(locSoup):
	good = False
	for tag in getTags(locSoup):
		if tag in taglist:
			good = True
			break
	return good

def testReviewCount(locSoup,n): #true if count >= n 
	if getReviewCount(locSoup) < n:
		return False
	else:
		return True

def testZip(locSoup,zipcode):
	if getZip(locSoup) == zipcode:
		return True
	else:
		return False

def findRestTag(locSoup):
	tags = getTags(locSoup)
	if 'Restaurants' in tags:
		return True
	else:
		return False

class Restaurant:
	def __init__(self,locSoup):
		zipcode = getZip(locSoup)
		reviewCount = getReviewCount(locSoup)
		rating = getRating(locSoup)
		tags = getTags(locSoup)
		name = locSoup.find_all('name')[0].text

def getRating(locSoup):
	return float(locSoup.rating.text)

def getTags(locSoup):
	tags = []
	for tag in locSoup.tags.find_all('tag'):
		tags.append(tag.string)
	return tags

def getZip(locSoup):
	return int(locSoup.address.postal_code.text)

def getReviewCount(locSoup):
	return int(locSoup.user_review_count.text)

def signURL(restName,zipcode,lat,lon):
	# Fill in these values	
	consumer_key = 'CqhLC2QPuVfCdlqKPyZG0Q'
	consumer_secret = 'E9HuPwKEQnYFrxt_Os0mzYC2xJY'
	token = 'IOqZqoxQPpIfbdfVRZp4v_y-tr_E__Qs'
	token_secret = 'HGUw14IFNpOBR0lQdB6Ye5ipnTs'
	
	consumer = oauth2.Consumer(consumer_key, consumer_secret)
	url = 'http://api.yelp.com/v2/search?term=' + str(restName) + '&location=' + str(zipcode) + '&cll=' + str(lat) + ',' + str(long) + "&limit=40&category_filter='restaurants'"

	#print 'URL: %s' % (url,)

	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
	                      'oauth_timestamp': oauth2.generate_timestamp(),
	                      'oauth_token': token,
	                      'oauth_consumer_key': consumer_key})

	token = oauth2.Token(token, token_secret)

	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)

	signed_url = oauth_request.to_url()

	print str(signed_url)

def getYelpURL(name,zipcode,lat,lon,which):
	#name = name.replace('&amp;', '')
	#name = name.replace(' Inc','')
	if name.find(' ') != -1:
		name = '%20'.join(name.split(' '))
	#print name
	if which == 1:
		return 'http://api.yelp.com/business_review_search?term=' + name + '&lat=' + lat + '&long=' + lon + '&ywsid=B0JWCs0q3i1kqyhcMK5gDA&category=restaurants'
	elif which == 2:
		return signURL(name,zipcode,lat,lon)

def yelp(yelpData, datastring):
	return yelpData['businesses'][0][datastring]

def getPercentDiff(name1, name2):
	if (not name1) or (not name2):
		return 0
	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	list1 = name1.split(' ')
	list2 = name2.split(' ')

	for word in list1:
		if word in list2:
			count1+=1
		if name2.find(word) != -1:
			count3+=1
			name2 = name2.replace(word,'',1)
	for word in list2:
		if word in list1:
			count2+=1
		if name1.find(word) != -1:
			count4+=1
			name1 = name1.replace(word,'',1)

	return max(float(count1)/len(list1),float(count2)/len(list2),float(count3)/len(list1),float(count4)/len(list2))

