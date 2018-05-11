import csv     # imports the csv module
import sys 
# CART on the Bank Note dataset
from random import seed
from random import randrange
from csv import reader
import dbInfo as di
import numpy as np
import numpy
import tfIdfCalc as idf
import dbInfo as db
import probFeedback as pf
import tfCalc as tf
import random
trainingSet=[]
testSet=[]
def loadDataset(filename, trainingSet=[] , testSet=[]):
	test=[]
	with open(filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
	movies = di.getAllMovies()
	tagIds = di.getAllTags()
	allTagLen = len(tagIds)
	dataset_copy = [['' for i in range(allTagLen+1)] for j in range(len(movies))]
	idfMovArr = idf.idfMovieTag()
	for i in range(len(dataset)):
		idfVect = idf.tfIdfMovieTag(dataset[i][0], idfMovArr)
		for j in range(len(idfVect)):
			dataset_copy[i][j] = idfVect[j]
		dataset_copy[i][allTagLen]=dataset[i][1]
		trainingSet.append(dataset_copy[i])
	train = [0 for i in range(len(dataset))]
	for i in range(len(dataset)):
		train[i] = int(dataset[i][0])
	k=0
	labels = ['0', '1']
	testset_copy = [['' for i in range(allTagLen+1)] for j in range(len(movies)-len(train))]
	for i in range(len(movies)):
			if(int(movies[i][0]) in train):
				pass
			else:
				test.append(movies[i][0])
				idfVect1 = idf.tfIdfMovieTag(movies[i][0], idfMovArr)
				for j in range(len(idfVect1)):
					testset_copy[k][j] = idfVect1[j]
				#testset_copy[k][allTagLen]=db.getMovieGenre(movies[i][0])[0]
				testset_copy[k][allTagLen]=random.choice(labels)
				testSet.append(testset_copy[k])
				k=k+1
	return test,trainingSet,testSet
	

def decTree():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.5
	test,trainingSet, testSet=loadDataset('foo.csv', trainingSet, testSet)
	#print('training: ',trainingSet[10])
	# generate predictions
	return test,trainingSet,testSet
	
# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
 
# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
def evaluate_algorithm(trainingSet,testSet, algorithm, *args):
	scores = list()
	predicted = algorithm(trainingSet, testSet, *args)
	print(predicted)
	actual = [row[-1] for row in testSet]
	accuracy = accuracy_metric(actual, predicted)
	scores.append(accuracy)
	return scores
 
def test_split(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
 
def gini_index(groups, classes):
	# count all samples at split point
	n_instances = float(sum([len(group) for group in groups]))
	# sum weighted Gini index for each group
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		# score the group based on the score for each class
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / n_instances)
	return gini
 
# Select the best split point for a dataset
def get_split(dataset):
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = test_split(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}
 
# Create a terminal node value
def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)
 
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return
	# check for max depth
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	# process left child
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], max_depth, min_size, depth+1)
	# process right child
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], max_depth, min_size, depth+1)
 
# Build a decision tree
def build_tree(train, max_depth, min_size):
	root = get_split(train)
	split(root, max_depth, min_size, 1)
	return root
 
# Make a prediction with a decision tree
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
 
# Classification and Regression Tree Algorithm
def decision_tree(train, test, max_depth, min_size):
	tree = build_tree(train, max_depth, min_size)
	predictions = list()
	
	for row in test:
		prediction = predict(tree, row)
		predictions.append(prediction)
	return(predictions)

# Test CART on Bank Note dataset
seed(1)
test,trainingSet, testSet = decTree()
print(test)
# evaluate algorithm
max_depth = 5
splits = 0.2
min_size = 10
scores = evaluate_algorithm(trainingSet, testSet, decision_tree, max_depth, min_size)
