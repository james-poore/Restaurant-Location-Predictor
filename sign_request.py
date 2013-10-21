import oauth2

def signURL(restName,zipcode,lat,lon)
	# Fill in these values	
	consumer_key = 'CqhLC2QPuVfCdlqKPyZG0Q'
	consumer_secret = 'E9HuPwKEQnYFrxt_Os0mzYC2xJY'
	token = 'IOqZqoxQPpIfbdfVRZp4v_y-tr_E__Qs'
	token_secret = 'HGUw14IFNpOBR0lQdB6Ye5ipnTs'
	
	consumer = oauth2.Consumer(consumer_key, consumer_secret)
	url = 'http://api.yelp.com/v2/search?term=bars&location=sf'

	print 'URL: %s' % (url,)

	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
	                      'oauth_timestamp': oauth2.generate_timestamp(),
	                      'oauth_token': token,
	                      'oauth_consumer_key': consumer_key})

	token = oauth2.Token(token, token_secret)

	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)

	signed_url = oauth_request.to_url()

	print 'Signed URL: %s' % (signed_url,)
