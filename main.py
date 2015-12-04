import sys, os, os.path, time, collections
import json
import re
import twitterAccess as tw
from TwitterAPI import TwitterAPI

numTweets = 10000
trackTweets = ['#Fallout4', '#LeagueofLegends,#lolesports', '#GTAV,#GTA5', '#Witcher3',\
'#CallofDutyBlackOps3', '#Minecraft', '#Skyrim', '#Halo5', '#CounterStrike,#CSGO', '#Trove']
tags = '#Fallout4,#LeagueofLegends,#lolesports,#GTAV,#GTA5,\
##Witcher3,#CallofDutyBlackOps3,#Minecraft,#Skyrim,#Halo5,#CounterStrike,#CSGO,#Trove'

gameNames = ['Grand Theft Auto V', 'Counter-Strike: Global Offensive', 'The Elder Scrolls V: Skyrim', 'Rocket League', 'The Witcher 3: Wild Hunt', 'Trove']

trainFiles = ['./tweets/train/gta5Train.json', './tweets/train/counterstrikeTrain.json', './tweets/train/skyrimTrain.json',\
'./tweets/train/rocketleagueTrain.json', './tweets/train/witcher3Train.json', './tweets/train/troveTrain.json']

testFiles = ['./tweets/test/gta5Test.json', './tweets/test/counterstrikeTest.json', './tweets/test/skyrimTest.json',\
'./tweets/test/rocketleagueTest.json', './tweets/test/witcher3Test.json', './tweets/test/troveTest.json']

files = ['./tweets/gta5.json', './tweets/counterstrike.json', './tweets/skyrim.json',\
'./tweets/rocketleague.json', './tweets/witcher3.json', './tweets/trove.json']

foldingFiles = ['./tweets/k-folding/counterstrike.json', './tweets/k-folding/gta5.json', './tweets/k-folding/rocketleague.json',\
'./tweets/k-folding/skyrim.json', './tweets/k-folding/witcher3.json', './tweets/k-folding/trove.json']

trainThreshold = time.strptime("Tue Aug 11 00:00:00 +0000 2015", "%a %b %d %H:%M:%S +0000 %Y")

# Download tweets separated into single archive file for future data purposes
def downloadTweets():
	api = TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_token, tw.access_token_secret)

	f = open('./archive/' + time.strftime("%b-%d-%Y") + '.json', 'w')

	r = api.request('statuses/filter', {'track': tags})
	count = 0
	for item in r:
		if count % 100 == 0: print count
		if count == numTweets: break
		if 'delete' in item: continue
		f.write(json.dumps(item))
		f.write('\n')
		count += 1

	# counts = collections.Counter()
	# count = 0

	# totalGoal = len(trackTweets) * numTweets

	# for item in r: #download and save to array
	# 	if count % 100 == 0: print count, totalGoal
	# 	if totalGoal == 0: break
	# 	if 'delete' in item: continue
	# 	for game in trackTweets:
	# 		if any(tag in item['text'] for tag in game.split(',')):
	# 			if counts[game] < numTweets:
	# 				counts[game] += 1
	# 				totalGoal -= 1
	# 				f.write(json.dumps(item))
	# 				f.write('\n')
	# 			break
	# 	count += 1

	f.close

	print "SAVED TRAIN AND TEST TWEETS TO FILE"


# Read in tweets from the dataset and search for occurrences of the hashtags for each
# of the games in the text. If it appears, write that json object to our outfile (either
# train or test based on the time stamp for the provided tweet).
# This is our filtering mechanism for getting tweets older than the time that the
# TwitterAPI allows for.
def filterTweetsOnHashtag():
	gta = open(files[0], 'w')
	cs = open(files[1], 'w')
	skyrim = open(files[2], 'w')
	rocket = open(files[3], 'w')
	witcher = open(files[4], 'w')
	trove = open(files[5], 'w')

	# gtaTest = open(testFiles[0], 'w')
	# csTest = open(testFiles[1], 'w')
	# skyrimTest = open(testFiles[2], 'w')
	# rocketTest = open(testFiles[3], 'w')
	# witcherTest = open(testFiles[4], 'w')
	# troveTest = open(testFiles[5], 'w')

	#Go through all of the files and create our outfile
	for root, _, files in os.walk('./07/'):
		for f in files:
			if not f.endswith(".json"): continue

			filename = os.path.join(root, f)
			if ".AppleDouble" in filename: continue
			print filename
			with open(filename, 'r') as d:
				for line in d:
					item = json.loads(line)

					if 'delete' in item: continue # Skip items that have been deleted
					text = item['text']
					if re.findall(r'(#gta5\b|#gtav\b)', text, re.IGNORECASE):
						print "gta"
						gta.write(json.dumps(item))
						gta.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	gta.write(json.dumps(item))
						# 	gta.write('\n')
						# else:
						# 	gtaTest.write(json.dumps(item))
						# 	gtaTest.write('\n')
					elif re.findall(r'(#counterstrike\b|#csgo\b)', text, re.IGNORECASE):
						print "cs"
						cs.write(json.dumps(item))
						cs.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	cs.write(json.dumps(item))
						# 	cs.write('\n')
						# else:
						# 	csTest.write(json.dumps(item))
						# 	csTest.write('\n')
					elif re.findall(r'#skyrim\b', text, re.IGNORECASE):
						print "skyrim"
						skyrim.write(json.dumps(item))
						skyrim.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	skyrim.write(json.dumps(item))
						# 	skyrim.write('\n')
						# else:
						# 	skyrimTest.write(json.dumps(item))
						# 	skyrimTest.write('\n')
					elif re.findall(r'#rocketleague\b', text, re.IGNORECASE):
						print "rocketleague"
						rocket.write(json.dumps(item))
						rocket.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	rocket.write(json.dumps(item))
						# 	rocket.write('\n')
						# else:
						# 	rocketTest.write(json.dumps(item))
						# 	rocketTest.write('\n')
					elif re.findall(r'#witcher3\b', text, re.IGNORECASE):
						print "witcher"
						witcher.write(json.dumps(item))
						witcher.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	witcher.write(json.dumps(item))
						# 	witcher.write('\n')
						# else:
						# 	witcherTest.write(json.dumps(item))
						# 	witcherTest.write('\n')
					elif re.findall(r'#trove\b', text, re.IGNORECASE):
						print "trove"
						trove.write(json.dumps(item))
						trove.write('\n')
						# if time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y") <= trainThreshold: #put into train
						# 	trove.write(json.dumps(item))
						# 	trove.write('\n')
						# else:
						# 	troveTest.write(json.dumps(item))
						# 	troveTest.write('\n')

	gta.close
	cs.close
	skyrim.close
	rocket.close
	witcher.close
	trove.close

	# gtaTest.close
	# csTest.close
	# skyrimTest.close
	# rocketTest.close
	# witcherTest.close
	# troveTest.close

	print "FINISHED FILTERING FILES"


# Extract features from the files, for both train and test
def extractFeatures():
	trainResults = {}
	testResults = {}

	playerCounts = []
	with open('game_stats.json') as f:
		playerCounts = json.load(f)

	for index, game in enumerate(gameNames):
		features = []
		users = [set()] * 31 # init each day in the set to have empty set of names
		tweetCounts = collections.Counter() # init each day in the set to have 0 tweets
		favoriteCounts = collections.Counter() # init each day in the set to have 0 follower count
		followerCounts = collections.Counter() # init each day in the set to have 0 follower count
		retweetCounts = collections.Counter() # init each day in the set to have 0 retweets

		'''
		Possible new features: Tag all games with the appropriate genres
		genre = {'GTAV': 'FPS'}
		nonlinear relationships between number of tweetCounts and number of playerCounts
		'''


		countIndex = [i for i, val in enumerate(playerCounts) if val["Game"] == game][0]

		with open(trainFiles[index]) as d:
			for line in d:
				item = json.loads(line)
				t = time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
				day = t.tm_mday - 1 #get day minus one for index

				if item['user']['screen_name'] not in users[day]:
					retweetCounts[day] += item['retweet_count']
					users[day].add(item['user']['screen_name'])

				tweetCounts[day] += 1 #increment tweet counts for this day
				favoriteCounts[day] += item['favorite_count']
				followerCounts[day] += item['user']['followers_count']


		with open(testFiles[index]) as d:
			for line in d:
				item = json.loads(line)
				t = time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
				day = t.tm_mday - 1 #get day minus one for index

				if item['user']['screen_name'] not in users[day]:
					retweetCounts[day] += item['retweet_count']
					users[day].add(item['user']['screen_name'])

				tweetCounts[day] += 1 #increment tweet counts for this day
				favoriteCounts[day] += item['favorite_count']
				followerCounts[day] += item['user']['followers_count']

		# Build the feature vector for each day
		for i in xrange(31):
			favAvg = float(favoriteCounts[i]) / tweetCounts[i] if tweetCounts[i] > 0 else 0
			followAvg = float(followerCounts[i]) / len(users[i]) if len(users[i]) > 0 else 0
			retweetAvg = float(retweetCounts[i]) / tweetCounts[i] if tweetCounts[i] > 0 else 0
			feat = [tweetCounts[i], len(users[i]), favAvg, followAvg, retweetAvg]
			#feat = [tweetCounts[i]] 	# Baseline
			formatDate = '08/' + (('0' + str(i+1)) if i+1 < 10 else str(i+1)) + '/15'
			features.append((feat, playerCounts[countIndex]["Peak Player"][formatDate]))

		trainResults[game] = features[:10]
		testResults[game] = features[10:]

	return (trainResults, testResults)


#Extract features from the files for each game, for use with folding
def extractFeaturesFolding(training, validation):
	trainResults = {}
	testResults = {}

	playerCounts = []
	with open('game_stats.json') as f:
		playerCounts = json.load(f)

	for index, game in enumerate(gameNames):
		features = []
		users = [set()] * 31 # init each day in the set to have empty set of names
		tweetCounts = collections.Counter() # init each day in the set to have 0 tweets
		favoriteCounts = collections.Counter() # init each day in the set to have 0 follower count
		followerCounts = collections.Counter() # init each day in the set to have 0 follower count
		retweetCounts = collections.Counter() # init each day in the set to have 0 retweets

		countIndex = [i for i, val in enumerate(playerCounts) if val["Game"] == game][0]

		with open(foldingFiles[index]) as d:
			for line in d:
				item = json.loads(line)
				t = time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
				day = t.tm_mday - 1 #get day minus one for index

				if item['user']['screen_name'] not in users[day]:
					retweetCounts[day] += item['retweet_count']
					users[day].add(item['user']['screen_name'])

				tweetCounts[day] += 1 #increment tweet counts for this day
				favoriteCounts[day] += item['favorite_count']
				followerCounts[day] += item['user']['followers_count']

		# Build the feature vector for each day
		for i in xrange(31):
			favAvg = float(favoriteCounts[i]) / tweetCounts[i] if tweetCounts[i] > 0 else 0
			followAvg = float(followerCounts[i]) / len(users[i]) if len(users[i]) > 0 else 0
			retweetAvg = float(retweetCounts[i]) / tweetCounts[i] if tweetCounts[i] > 0 else 0
			feat = [tweetCounts[i], len(users[i]), favAvg, followAvg, retweetAvg]
			formatDate = '08/' + (('0' + str(i+1)) if i+1 < 10 else str(i+1)) + '/15'
			features.append((feat, playerCounts[countIndex]["Peak Player"][formatDate]))

		#take only the days that we are currently taking a look at
		trainResults[game] = [features[i] for i in training]
		testResults[game] = [features[i] for i in validation]

	return (trainResults, testResults)


if __name__ == "__main__":
	downloadTweets()

