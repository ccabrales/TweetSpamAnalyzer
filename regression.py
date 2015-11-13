# Rum Linear Regression on the sets
import numpy as np
#import statsmodels.api as sm
 
trainingData = dict()
trainingData['GTAV'] = [([20, 2, 1], 12321), ([10, 4, 3], 142553), ([15, 3, 2], 89247)]

testData = dict()

def stackArrays(features):
	numFeatures = len(features[0])
	print numFeatures
	stacked = []
	for i in range(numFeatures):
		stack = []
		for feature in features:
			stack.append(feature[i])
		stacked.append(stack)
	return stacked 

results = None
# Train the linear regression model
for game in trainingData:
	# Array of tuples ([feature vector], value)
	numSample = len(trainingData[game])
	x_train = []
	y_train = []
	for feature, value in trainingData[game]:
		x_train.append(feature)
		y_train.append(value)
	x_train = stackArrays(x_train)
	x_train = sm.add_constant(x_train)
	model = sm.OLS(y, X)
	results = model.fit()
	print(results.summary())



params = results.params
constant = params[-1]
weights = result[:len(params)-1]
# Test model
for game in testData:
	percentError = []
	for feature, value in testData[game]:
		# put into regression equation
		y_predicted = constant
		for i in range(len(feature)):
			y_predicted += feature[i]*weights[i]
		# Determine error
		error = 1.0 * math.abs(y_predicted - value) / value
	print "Game: ", game
	print "Test Error ", percentError
	print "Average Error ", sum(percentError)/len(percentError) 
