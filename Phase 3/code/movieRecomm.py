import dbInfo as di
import utils
import lda
import sys
from operator import itemgetter
import tensorDecomp as td
import persPageRank as ppr
import tfCalc as tf
import tfIdfCalc as idf
import numpy as np
from scipy.stats import mode

movies = di.getAllMovies()
tagIds = di.getAllTags()
allTagLen = len(tagIds)
movieLen = len(movies)

def formSvdMat(numSemantics):
	mat = np.zeros((movieLen,allTagLen))
	if(len(mat)<numSemantics or len(mat[0])<numSemantics):
		print("cant report top semantics")
		sys.exit()
	idfMovArr = idf.idfMovieTag()
	for i in range(movieLen):
		mat[i] = idf.tfIdfMovieTag(movies[i][0], idfMovArr)
	U, s, V = np.linalg.svd(mat,full_matrices=False)
	movieFacts = np.zeros((movieLen, numSemantics))
	for i in range(movieLen):
		for j in range(numSemantics):
			movieFacts[i][j] = U[i][j]
	return movieFacts

def formPcaMat(numSemantics):
	mat = np.zeros((movieLen,allTagLen))
	if(len(mat)<numSemantics or len(mat[0])<numSemantics):
		print("cant report top semantics")
		sys.exit()
	idfMovArr = idf.idfMovieTag()
	for i in range(movieLen):
		mat[i] = idf.tfIdfMovieTag(movies[i][0], idfMovArr)
	matrix = np.matmul(mat,np.transpose(mat))
	U, s, V = np.linalg.svd(matrix, full_matrices=False)
	movieFacts = np.zeros((movieLen, numSemantics))
	for i in range(movieLen):
		for j in range(numSemantics):
			movieFacts[i][j] = U[i][j]
	return movieFacts

def formLdaMat(numSemantics):
	movies1 = tuple(movies)
	actors = di.getAllActors()
	actors1 = tuple(actors)
	actLen = len(actors)
	
	movAct = []
	for movie in movies1:
		arr = []
		for i in range(0,actLen):
			arr.append(0)
		acts = tuple(di.getMovieActorIds(movie[0]))
		for actor in actors1:
			for act in acts:
				if actor == act:
					arr[actors1.index(actor)] = 1
		movAct.append(arr)
	movAct = np.array(movAct)
	model = lda.LDA(n_topics = numSemantics, n_iter = 100, random_state = 1)
	model.fit(movAct)
	#component = model.components_
	return model.doc_topic_

def formLdaMat1(numSemantics):
	movies1 = tuple(movies)
	tags1 = tuple(tagIds)

	movTag = []
	for movie in movies1:
		arr = []
		for i in range(allTagLen):
			arr.append(0)
		tgs = tuple(di.getMovieTags(movie[0]))
		for tag in tags1:
			for tg in tgs:
				if tag[0] == tg[0]:
					arr[tags1.index(tag)] += 1
		movTag.append(arr)
	movTag = np.array(movTag)
	#print(movTag)
	model = lda.LDA(n_topics = numSemantics, n_iter = 100, random_state = 1)
	model.fit(movTag)
	return model.doc_topic_

def formTensMat():
	#vect, actors, movies, years = td.vectActMovYr()
	vect, actors, movies, years = td.vectActMovTag()
	tens = td.vectToTens(vect)
	print("\n\ntensor formed\nShape =",tens.shape)
	numSemantics = min(tens.shape)//2
	factors = td.tensDecomp(tens, numSemantics)
	print("\ntensor decomposed\n")
	return factors[1]

def formPPRMatrix():
	mat = np.zeros((movieLen,allTagLen))
	idfMovArr = idf.idfMovieTag()
	for i in range(len(movies)):
		mat[i] = idf.tfIdfMovieTag(movies[i][0], idfMovArr)
	return mat

def pprRes(matrix, seeds):
	seedMat = ppr.formSeed(seeds, movies)
	pprOut = ppr.personalizedPageRank(matrix, seedMat, 0.15)
	return ppr.rankedList(pprOut, movies, seeds, movieLen)

def formQueryVect(mat, userId):
	movTimes = []
	usrMovies = []
	movTimeVect = {}
	queryVect = np.zeros(len(mat[0]))

	usrSeenMovies = di.getusrMovTime(userId)
	if(len(usrSeenMovies) <= 0):
		print("user has not watched any movies to give suggestions")
		sys.exit()
	for mov in usrSeenMovies:
		usrMovies.append(mov[0])
		movTimes.append(mov[1])
	movTimes = sorted(range(len(movTimes)),key=lambda x:movTimes[x])

	for i in range(len(usrMovies)):
		movTimeVect[usrMovies[i]] = movTimes[i]
	for i in range(len(movies)):
		if(movies[i][0] in usrMovies):
			#print(movTimeVect[movies[i][0]])
			queryVect = queryVect + (movTimeVect[movies[i][0]]+1)*mat[i]
	queryVect = queryVect/len(usrMovies)
	print("Query Vector =")
	utils.printVect(queryVect)
	return (queryVect, usrMovies)

def formNewSeeds(seeds, rankedRes, relMoviesIdx):
	newSeeds = []
	for seed in seeds:
		newSeeds.append(seed)
	relMov = []
	for i in range(movieLen):
		if(str(i) in relMoviesIdx):
			relMov.append(rankedRes[i-1])
	for i in range(movieLen):
		if(movies[i][0] in relMov):
			newSeeds.append(movies[i][0])
	return newSeeds

def getSimilarity(mat, query, usrMovies):
	res = {}
	for i in range(movieLen):
		if(movies[i][0] not in usrMovies):
			res[movies[i][0]] = np.dot(query, mat[i])
	ranks = utils.sortByValue(res)
	rankedRes = []
	for i in ranks:
		rankedRes.append(i[0])
	return rankedRes

def getRelIrrMov(rankedRes, relMoviesIdx, irrMoviesIdx):
	relMov = []
	irrMov = []
	for i in range(len(rankedRes)+1):
		if(str(i) in relMoviesIdx):
			relMov.append(rankedRes[i-1])
		if(str(i) in irrMoviesIdx):
			irrMov.append(rankedRes[i-1])
	relMovies = []
	irrMovies = []
	for i in range(movieLen):
		if(movies[i][0] in relMov):
			relMovies.append(i)
		if(movies[i][0] in irrMov):
			irrMovies.append(i)
	return (relMovies, irrMovies, irrMov)

def getNewIdx(list1,list2,relMoviesIdx,irrMoviesIdx):
	relMovies = []
	irrMovies = []
	for relMov in relMoviesIdx:
		relMovies.append(list2.index[list1[relMov]])
	for irrMov in irrMoviesIdx:
		irrMovies.append(list2.index[list1[irrMov]])
	return (relMovies, irrMovies)
	
#Function to take out the measure that combines SVD, PCA, LDA, Tensor and PPR and recommends 5 Movies to the user
def rankCombine(arr1, arr2, arr3, arr4, arr5, usrMovies):
	list = []
	for mov in movies:
		if(mov[0] not in usrMovies):
			list.append(mov[0])
	arr_len = len(list)
	#print(arr_len,list)
	ranks = {}
	for i in range(arr_len):
		movie = list[i]
		#print(list[i])
		totRank = arr1.index(movie) + arr2.index(movie) + arr3.index(movie) + arr4.index(movie) + arr5.index(movie)
		#final_ranks = mode([rank1[i],rank2[i],rank3[i],rank4[i],rank5[i]])[0][0]
		ranks[movie] = totRank/5
	finalRanks = sorted(ranks.items(), key=itemgetter(1))
	#print("final ranks =",finalRanks)
	list = []
	for mov in finalRanks:
		list.append(mov[0])
	return list