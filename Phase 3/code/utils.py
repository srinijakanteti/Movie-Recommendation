from operator import itemgetter
import dbInfo as di
import numpy as np
from scipy.cluster.vq import kmeans2, whiten

# This function calculates the weight based on the date
# i.e. newer date gets higher weight and older date gets less weight
# Input to this is date in 'yyyy-mm-dd' and time in 'hh:mm:ss' format (both are in string formats)
# Output is the weight based on time calculated as
# weight = (year/100)*(month/12)*(day/31)*((hour+1)/24)*((min+1)/60)*((sec+1)/60)
def wieghtedTime(date, time):
	(yr,mn,day) = date.split("-")
	yr = int(yr)
	mn = int(mn)
	day = int(day)
	# Add 1 to avoid 0th hour, minute and second
	(hr,min,sec) = time.split(":")
	hr = int(hr)+1
	min = int(min)+1
	sec = int(sec)+1
	return (yr*mn*day*hr*min*sec)/(3214080000)

def weightedRank(rank):
	return 1/rank

def sortByValue(vector):
	return sorted(vector.items(), key=itemgetter(1), reverse=True)
	
def roundOfValues(vector):
	retVector = {}
	for entry in vector:
		retVector[entry[0]] = round(entry[1], 5)
	return retVector

def normalizeVector(vector):
	sum = 0
	retVector = {}
	for entry in vector:
		sum = sum + abs(entry[1])
	if (sum == 0):
		return vector
	for entry in vector:
		val = entry[1]/sum
		retVector[entry[0]] = round(val, 5)
	return retVector

# Given a movie object this function returns the array for tf weights of all tags in order
def getGenreMovieTags(movie):
	tagIds = di.getAllTags()
	tagLen = len(tagIds)
	tfArray = [0 for i in range(tagLen)]
	unqTags = movie.getUnqTags()
	tags = movie.getTags()
	totalTags = len(tags)
	i = 0
	tfVect = {}
	for tagId in unqTags:
		tfFactor = 0
		for tag in tags:
			if(tag.getId() == tagId):
				tfFactor = tfFactor + tag.getTimeWeight()
		tfVect[tagId] = tfFactor/totalTags
	for i in range(tagLen):
		if(tagIds[i][0] in tfVect.keys()):
			tfArray[i] = tfVect[tagIds[i][0]]
	return tfArray

def rankSem(arr, list):
	vect = ""
	length = len(arr)
	d={}
	for i in range(length):
		if(arr[i] != 0):
			d[list[i][0]] = arr[i]
	d = sortByValue(d)
	return normalizeVector(d)

def printVect(arr):
	semantics = {}
	for i in range(len(arr)):
		sem = "sem" + str(i+1)
		semantics[sem] = arr[i]
	semantics = sortByValue(semantics)
	print(semantics)
	
	
def form_groups_semantics(matrix,list,grps):
	whitenedmat = whiten(matrix)
	#list=db.getAllActorNames()
	centroids,distortion = kmeans2(whitenedmat, grps, minit = 'points')
	groups = [[0 for i in range(0,2)]for j in range(0,matrix.shape[0])]
	d = {}
	for i in range(matrix.shape[0]):
		d[list[i][0]] = distortion[i]
	groups = {}
	for key, value in sorted(d.items()):
		groups.setdefault(value, []).append(key)
	return groups