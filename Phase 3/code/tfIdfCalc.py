import utils
import numpy as np
import tfCalc
import dbInfo as di
import math
np.set_printoptions(threshold=np.nan)


def idfActorTag():
	idfActVect = {}
	allTags = di.getAllTags()
	allActors = di.getAllActors()
	actorCount = len(allActors)
	for tag in allTags:
		tagCount = 0
		idfActVect[tag[0]] = 0
		for actor in allActors:
			tags = di.getActorTags(actor[0])
			if(tag[0] in tags[0]):
				tagCount = tagCount + 1
		if(tagCount != 0):
			idfActVect[tag[0]] = math.log(actorCount/tagCount)
	#print(idfActVect)
	return idfActVect

def idfMovieTag():
	allTags = di.getAllTags()
	allMovies = di.getAllMovies()
	movieCount = len(allMovies)
	idfMovTagArr = np.zeros(len(allTags))
	movTags = []
	for mov in allMovies:
		movTags.append(di.getMovieTagIds(mov[0])[0][0].split(","))
	for i in range(len(allTags)):
		tagCount = 0
		for j in range(len(allMovies)):
			if(allTags[i][0] in movTags[j]):
				tagCount = tagCount + 1
		res = 0
		if(tagCount != 0):
			res = math.log(movieCount/tagCount)
		idfMovTagArr[i] = res
	#print(idfMovTagArr)
	return idfMovTagArr

def idfGenreTag():
	idfGenVect = {}
	allTags = di.getAllTags()
	allGenres = di.getAllGenres()
	genreCount = len(allGenres)
	for tag in allTags:
		tagCount = 0
		idfGenVect[tag[0]] = 0
		for genre in allGenres:
			tags = di.getGenreTags(genre[0])
			if(tag[0] in tags[0]):
				tagCount = tagCount + 1
		if(tagCount != 0):
			idfGenVect[tag[0]] = math.log(genreCount/tagCount)
	#print(idfGenVect)
	return idfGenVect

def idfUserTag():
	idfUserVect = {}
	allTags = di.getAllTags()
	allUsers = di.getAllUsers()
	userCount = len(allUsers)
	for tag in allTags:
		tagCount = 0
		idfUserVect[tag[0]] = 0
		for user in allUsers:
			tags = di.getUserTags(user[0])
			if(tag[0] in tags[0]):
				tagCount = tagCount + 1
		if(tagCount != 0):
			idfUserVect[tag[0]] = math.log(userCount/tagCount)
	#print(idfUserVect)
	return idfUserVect

def tfIdfActorTag(actorId, idfActVector):
	tfVector = tfCalc.tfActorTag(actorId)
	tfIdfVector = {}
	tags = tfVector.keys()
	for tag in tags:
		tfIdfVector[tag] = tfVector[tag]*idfActVector[tag]
	#print('actor',tfIdfVector)
	tfIdfVector = utils.sortByValue(tfIdfVector)
	return utils.normalizeVector(tfIdfVector)

def tfIdfMovieTag(movieId, idfMovArr):
	tfArr = tfCalc.tfMovTag(movieId)
	tfIdfArr = np.zeros(len(idfMovArr))
	for i in range(len(tfIdfArr)):
		tfIdfArr[i] = tfArr[i]*idfMovArr[i]
	return tfIdfArr

def tfIdfGenreTag(genre, idfGenVector):
	tfVector = tfCalc.tfGenreTag(genre)
	tfIdfVector = {}
	tags = tfVector.keys()
	for tag in tags:
		tfIdfVector[tag] = tfVector[tag]*idfGenVector[tag]
	#print('genre',tfIdfVector)
	tfIdfVector = utils.sortByValue(tfIdfVector)
	return utils.normalizeVector(tfIdfVector)

def tfIdfUserTag(userId, idfUserVector):
	tfVector = tfCalc.tfUserTag(userId)
	tfIdfVector = {}
	tags = tfVector.keys()
	for tag in tags:
		tfIdfVector[tag] = tfVector[tag]*idfUserVector[tag]
	#print('user',tfIdfVector)
	tfIdfVector = utils.sortByValue(tfIdfVector)
	return utils.normalizeVector(tfIdfVector)

#idfVect = idfMovieTag()
#tfIdfVect = tfIdfMovieTag('3189', idfVect)
#print((tfIdfVect))