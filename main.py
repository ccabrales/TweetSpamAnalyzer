import sys, os, os.path
import json
import re
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 10
trackTweets = ['Fallout4', 'LeagueofLegends,lolesports', 'Football Manager', 'FIFA16,FIFA', "Assasin'sCreedSyndicate", 'GTAV,GTA5', 'ChibiRobo',\
'NBALive', 'PlantsVSZombies', 'DarkSouls2,DarkSoulsII', 'DiabloIII,Diablo3', 'Destiny', 'Witcher3', 'RideToHellRetribution', 'Hypervoid', 'Borderlands',\
'CallofDutyBlackOps3', 'TonyHawkProSkater5', 'Minecraft', 'Skyrim', 'LegendOfZelda', 'Halo5', 'Starcraft2,StarcraftII', 'CounterStrike', 'SonictheHedgehog']

# DEPRECATED - Old method used to download tweets in firehose method
# def saveTweets():
# 	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

# 	r = api.request('statuses/filter', {'track': trackTweets[0]})
# 	count = 0
# 	trainTweets = []
# 	testTweets = []

# 	train = open(trainfilename, 'w')
# 	test = open(testfilename, 'w')
# 	for item in r:
# 		if count == numTweets: break
# 		if 'delete' in item:
# 			continue
# 		if count < 5:
# 			trainTweets.append(json.dumps(item))
# 		else:
# 			testTweets.append(json.dumps(item))
# 		count += 1

# 	train.write("[")
# 	train.write(",\n".join(trainTweets))
# 	train.write("]")
# 	train.close

# 	test.write("[")
# 	test.write(",\n".join(testTweets))
# 	test.write("]")
# 	test.close
# 	print "SAVED TO FILE"

# Download tweets separated into categories/games
def downloadTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	for i in xrange(len(trackTweets)):
		r = api.request('statuses/filter', {'track': trackTweets[i], 'since':2014-07-19})
		# r = api.request('search/tweets', {'q': '#LeagueOfLegends', 'since': '2014-11-03', 'until': '2014-11-11'})
		count = 0
		trainTweets = []
		testTweets = []

		trainfilename = 'tweets/train/' + trackTweets[i] + 'Train.json'
		testfilename = 'tweets/test/' + trackTweets[i] + 'Test.json'
		train = open(trainfilename, 'w')
		test = open(testfilename, 'w')

		for item in r: #download and save to array
			if count == numTweets: break
			if 'delete' in item: continue
			if count < numTweets / 3:
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

	print "SAVED TRAIN AND TEST TWEETS TO FILE"



# Read in tweets from the dataset and search for occurrences of the hashtags for each
# of the games in the text. If it appears, write that json object to our outfile so.
# This is our filtering mechanism for getting tweets older than the time that the
# TwitterAPI allows for.
def filterTweetsOnHashtag():
	gta = open('./tweets/gta5.json', 'w')
	cs = open('./tweets/counterstrike.json', 'w')
	skyrim = open('./tweets/skyrim.json', 'w')
	rocket = open('./tweets/rocketleague.json', 'w')
	witcher = open('./tweets/witcher3.json', 'w')
	trove = open('./tweets/trove.json', 'w')

	#Go through all of the files and create our outfile
	for root, _, files in os.walk('./08/'):
		for f in files:
			if not f.endswith(".json"): continue

			filename = os.path.join(root, f)
			with open(filename, 'r') as d:
				for line in d:
					item = json.loads(line)

					if 'delete' in item: continue # Skip items that have been deleted
					text = item['text']
					if re.findall(r'(#gta5\b|#gtav\b)', text, re.IGNORECASE):
						print "gta"
						gta.write(json.dumps(item))
						gta.write('\n')
					elif re.findall(r'(#counterstrike\b|#csgo\b)', text, re.IGNORECASE):
						print "cs"
						cs.write(json.dumps(item))
						cs.write('\n')
					elif re.findall(r'#skyrim\b', text, re.IGNORECASE):
						print "skyrim"
						skyrim.write(json.dumps(item))
						skyrim.write('\n')
					elif re.findall(r'#rocketleague\b', text, re.IGNORECASE):
						print "rocketleague"
						rocket.write(json.dumps(item))
						rocket.write('\n')
					elif re.findall(r'#witcher3\b', text, re.IGNORECASE):
						print "witcher"
						witcher.write(json.dumps(item))
						witcher.write('\n')
					elif re.findall(r'#trove\b', text, re.IGNORECASE):
						print "trove"
						trove.write(json.dumps(item))
						trove.write('\n')

	gta.close
	cs.close
	skyrim.close
	rocket.close
	witcher.close
	trove.close

	print "FINISHED FILTERING FILES"



def trainTweets():
	data = []
	with open(trainfilename, 'r') as f:
		data = json.load(f)


def testTweets():
	data = []
	with open(testfilename, 'r') as f:
		data = json.load(f)

if __name__ == "__main__":
	filterTweetsOnHashtag()