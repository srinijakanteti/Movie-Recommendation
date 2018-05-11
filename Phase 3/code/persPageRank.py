import numpy as np
import dbInfo as db
import utils
from sklearn.preprocessing import normalize
import warnings
warnings.filterwarnings("ignore")

def diff(mat1,mat2):
	trigger = sumval = diff = 0
	for i in range(len(mat1)):
		diff = abs(mat1[i] - mat2[i])
		sumval = sumval + diff
	if(sumval > 0.001):
		trigger = 1
	return trigger

def personalizedPageRank(matrix, normSeed, a):
	matrix = normalize(matrix, axis=0)
	#print("matrix = ", matrix)
	prob = np.zeros(matrix.shape[0])
	probn = np.ones(matrix.shape[0])
	c = 0
	while( diff(prob,probn) and (c <= 10) ):
		c += 1
		#print("c=",prob)
		prob = probn
		prob = prob/(np.sum(prob))
		#print(prob)
		probn = a*np.matmul(matrix,prob) + (1-a)*normSeed
	#print("prob = ", probn)
	return probn

def rankedList(arr, list, seeds, n):
	d = {}
	#print("before srt =",arr,list)
	for i in range(len(arr)):
		d[list[i][0]] = arr[i]
	sortedList = utils.sortByValue(d)
	#print(sortedList)
	retList = []
	k=0
	for i in range(len(arr)):
		if(sortedList[i][0] not in seeds):
			k += 1
			retList.append(sortedList[i][0])
		if(k>=n):
			break
	#print("s = ",retList)
	return retList

def formSeed(seedList, allIds):
	normSeed = np.zeros(len(allIds))
	for i in range(len(normSeed)):
		if(allIds[i][0] in seedList):
			#print("in if loop", allIds[i][0])
			normSeed[i] = 1#/len(seedList)
	return normSeed
