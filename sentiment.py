import nltk as nltk
import csv
import re

# Code based on implementation shown on "http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/#sampletweets-csv"

trainFile = "./sentiment_data/training.1600000.processed.noemoticon.csv"
featureList = []

def getFeatureVector(tweet):
	featureVector = set(tweet.split())
	return featureVector

def processTweet(tweet):
	# Borrowed from 
	# Convert to lower case
	tweet = tweet.lower() 
	# Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	return tweet

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def trainClassifier(featureList):
	trainingTweets = csv.reader(open(trainFile, 'rb'), delimiter=',', quotechar='|')
	tweets = []
	count = 0
	for row in trainingTweets:
		sentiment = row[0]
		tweet = ''.join(row[5:])
		tweet = processTweet(tweet)
		featureVector = getFeatureVector(tweet)
		featureList.extend(featureVector)
		tweets.append((featureVector, sentiment))
	featureList = list(set(featureList))
	training_set = nltk.classify.util.apply_features(extract_features, tweets)
	return nltk.NaiveBayesClassifier.train(training_set)

#	classifier = extractProcessTweets(featureList)
def classifyTweet(classifier, tweet):
	sentiment = classifier.classify(extract_features(getFeatureVector(processTweet(tweet))))
	return int(sentiment[1:len(sentiment)-1])