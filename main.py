import sys
import json
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 10
trainfilename = 'tweetsTrain2.json'
testfilename = 'tweetsTest2.json'
trainTrackTweets = ['Fallout4']
testTrackTweets = []

# DEPRECATED - Old method used to download tweets in firehose method
def saveTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	r = api.request('statuses/filter', {'track': trainTrackTweets[0]})
	count = 0
	trainTweets = []
	testTweets = []

	train = open(trainfilename, 'w')
	test = open(testfilename, 'w')
	for item in r:
		if count == numTweets: break
		if 'delete' in item:
			continue
		if count < 5:
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

# Download tweets separated into categories/games
def downloadTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	# Training tweets
	for i in xrange(len(trainTrackTweets)):
		r = api.request('statuses/filter', {'track': trainTrackTweets[i]})
		count = 0
		tweets = []
		filename = trainTrackTweets[i] + '.json'
		train = open(filename, 'w')

		for item in r:
			if count == numTweets: break
			if 'delete' in item: continue
			tweets.append(json.dumps(item))
			count += 1

		train.write("[")
		train.write(",\n".join(tweets))
		train.write("]")
		train.close

	# Test tweets
	for i in xrange(len(testTrackTweets)):
		r = api.request('statuses/filter', {'track': testrackTweets[i]})
		count = 0
		tweets = []
		filename = testTrackTweets[i] + '.json'
		test = open(filename, 'w')

		for item in r:
			if count == numTweets: break
			if 'delete' in item: continue
			tweets.append(json.dumps(item))
			count += 1

		test.write("[")
		test.write(",\n".join(tweets))
		test.write("]")
		test.close

	print "SAVED TRAIN AND TEST TWEETS TO FILE"

def trainTweets():
	data = []
	with open(trainfilename, 'r') as f:
		data = json.load(f)


def testTweets():
	data = []
	with open(testfilename, 'r') as f:
		data = json.load(f)