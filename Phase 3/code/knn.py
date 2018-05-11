
# Example of kNN implemented from Scratch in Python
 
import csv
import random
import math
import dbInfo as di
import tfIdfCalc as idf
import operator
import numpy
 
def loadDataset(filename, trainingSet=[] , testSet=[]):
	trainlist=[]
	test =[]
	with open(filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
	movies = di.getAllMovies()
	tagIds = di.getAllTags()
	allTagLen = len(tagIds)
	dataset_copy = [['' for i in range(allTagLen+1)] for j in range(len(dataset))]
	#dataset_copy = numpy.zeros((len(movies),allTagLen+1))
	#dataset_copy = [[0 for i in range(allTagLen+1)] for j in range(len(movies))]
	idfMovArr = idf.idfMovieTag()
	#print(idfMovArr)
	for i in range(len(dataset)):
		trainlist.append(dataset[i][0])
		idfVect = idf.tfIdfMovieTag(dataset[i][0], idfMovArr)
		for j in range(len(idfVect)):
			dataset_copy[i][j] = idfVect[j]
		dataset_copy[i][allTagLen]=dataset[i][1]
		trainingSet.append(dataset_copy[i])
	train = [0 for i in range(len(dataset))]
	for i in range(len(dataset)):
		train[i] = int(dataset[i][0])
	k=0
	#print(len(movies), len(train), "fdsf")
	labels = ['0', '1']
	testset_copy = [['' for i in range(allTagLen+1)] for j in range(len(movies))]
	for i in range(len(movies)):
			if(int(movies[i][0]) in train):
				pass
			else:
				test.append(movies[i][0])
				idfVect1 = idf.tfIdfMovieTag(movies[i][0], idfMovArr)
				for j in range(len(idfVect1)):
					testset_copy[k][j] = idfVect1[j]
				#testset_copy[k][allTagLen]=di.getMovieGenre(movies[i][0])[0]
				testset_copy[k][allTagLen]=random.choice(labels)
				testSet.append(testset_copy[k])
				k=k+1
	#print("train data =",trainingSet)
	#print("\n\n test data =",testSet)
	return trainingSet,testSet,trainlist,test

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k,trainlist):
	distances = []
	#print(testInstance)
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainlist[x], dist,trainingSet[x][-1]))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x])
	return neighbors
 
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def knn():
	# prepare data
	trainingSet=[]
	testSet=[]
	trainingSet, testSet,trainlist,test = loadDataset('foo1.csv',trainingSet, testSet)
	k = int(input("Enter number of neighbours to be considered:"))
	#print('training: ',trainingSet[10])
	# generate predictions
	predictions=[]
	print(len(test),len(testSet))
	for x in range(len(test)):
		neighbors = getNeighbors(trainingSet, testSet[x], k,trainlist)
		result = getResponse(neighbors)
		predictions.append(result)
		mvName = di.getMovName(test[x])
		print("for movie :",test[x],mvName[0]," > predicted=" ,repr(result))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')

knn()
