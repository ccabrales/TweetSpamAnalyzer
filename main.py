import sys
import json
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 10000
trainfilename = 'tweetsTrain.json'
testfilename = 'tweetsTest.json'

def saveTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	r = api.request('statuses/sample')
	count = 0
	trainTweets = []
	testTweets = []

	train = open(trainfilename, 'w')
	test = open(testfilename, 'w')
	for item in r:
		if count == numTweets: break
		if 'delete' in item:
			continue
		if count < 3000:
			trainTweets.append(json.dumps(item))
		else:
			testTweets.append(json.dumps(item))
		count += 1

	train.write("[")
	train.write(",\n".join(trainTweets))
	train.write("]")
	train.close

	test.write("[")
	test.write(",\n".join(testTweets))
	test.write("]")
	test.close
	print "SAVED TO FILE"

def trainTweets():
	data = []
	with open(trainfilename, 'r') as f:
		data = json.load(f)


def testTweets():
	data = []
	with open(testfilename, 'r') as f:
		data = json.load(f)