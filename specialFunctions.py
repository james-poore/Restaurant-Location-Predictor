from bs4 import BeautifulSoup
import oauth2

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
		tags.append(str(tag.text))
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
	count1 = 0
	count2 = 0
	list1 = name1.split(' ')
	list2 = name2.split(' ')

	for word in list1:
		if word in list2:
			count1+=1
	for word in list2:
		if word in list1:
			count2+=1

	return max(float(count1)/len(list1),float(count2)/len(list2))

