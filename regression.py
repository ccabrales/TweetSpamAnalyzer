#Includes linear regression

import numpy as np
import main
import statsmodels.api as sm
import pandas as pd
import collections


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

'''
y = [1,2,3,4,3,4,5,4,5,5,4,5,4,5,4,5,6,5,4,5,4,3,4]

x = [
     [4,2,3,4,5,4,5,6,7,4,8,9,8,8,6,6,5,5,5,5,5,5,5],
     [4,1,2,3,4,5,6,7,5,8,7,8,7,8,7,8,7,7,7,7,7,6,5],
     [4,1,2,5,6,7,8,9,7,8,7,8,7,7,7,7,7,7,6,6,4,4,4]
     ]

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

#print reg_m(y, x).summary()
'''

def kFoldCrossValidation(X, K):
	for k in xrange(K):
		training = [x for i, x in enumerate(X) if i % K != k]
		validation = [x for i, x in enumerate(X) if i % K == k]
		yield training, validation

def runLinearRegression():
	#set up k-folding here
	K = 6 #number of partitions
	# testSize = math.floor(31 / K)
	X = [i for i in xrange(31)]

	totalError = collections.Counter()
	totalPercentError = collections.Counter()

	for training, validation in kFoldCrossValidation(X, K):
		allData = main.extractFeaturesFolding(training, validation)

		trainingData = allData[0]
		testData = allData[1]

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
			#x_train = sm.add_constant(x_train)
			ones = np.ones(len(x_train[0]))
			X_train = sm.add_constant(np.column_stack((x_train[0], ones)))
			for ele in x_train[1:]: 
			       X_train = sm.add_constant(np.column_stack((ele, X_train)))

			model = sm.OLS(y_train, X_train)
			results = model.fit()
			print(results.summary())

			#Test
			params = results.params

			constant = params[-1]

			weights = params[1:]
			print weights
			# Test model
			percentError = []
			for feature, value in testData[game]:
			       # put into regression equation
			       #print feature, value
			       y_predicted = constant
			       for i in range(len(feature)):
			               y_predicted += feature[i]*weights[i]
			       # Determine error
			       print y_predicted
			       error = 1.0 * abs(y_predicted - value) / value
			       percentError.append(error)

			totalError[game] += sum(percentError)
			totalPercentError[game] += sum(percentError)/len(percentError)

			print "Game: ", game
			print "Test Error ", percentError
			print "Average Error ", sum(percentError)/len(percentError)

	for x in totalError: totalError[x]/=K
	for x in totalPercentError: totalPercentError[x]/=K

	for x in totalError:
		print "Total Error", x, totalError[x]
		print "Total Percent Error", x, totalPercentError[x]

# Execute the following
runLinearRegression()