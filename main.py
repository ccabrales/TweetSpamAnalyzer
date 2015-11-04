import sys
import json
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 10000
filename = 'tweets.json'

def saveTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	r = api.request('statuses/sample')
	count = 0
	tweets = []

	obj = open(filename, 'w')
	for item in r:
		if count == numTweets: break
		# if count == 0: print (item)
		tweets.append(json.dumps(item))
		count += 1

	obj.write("[")
	obj.write(",\n".join(tweets))
	obj.write("]")
	obj.close
	print "SAVED TO FILE"

def readTweets():
	data = []
	with open(filename, 'r') as f:
		data = json.load(f)