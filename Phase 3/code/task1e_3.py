import numpy as np
import dbInfo as di
import probFeedback as pf
import movieRecomm as mr

numSemantics = 20
numMovies = 5
userId = input("\nGive User Id: ")

movies = di.getAllMovies()
movieNames = di.getAllMovieNames()
moviesArr = []
for mov in movies:
	moviesArr.append(mov[0])

#1. for SVD
movieFactsSVD = mr.formSvdMat(numSemantics)
queryVectSVD, usrMovies = mr.formQueryVect(movieFactsSVD, userId)
rankedResSVD = mr.getSimilarity(movieFactsSVD, queryVectSVD, usrMovies)

#2. for PCA
movieFactsPCA = mr.formPcaMat(numSemantics)
queryVectPCA, usrMovies = mr.formQueryVect(movieFactsPCA, userId)
rankedResPCA = mr.getSimilarity(movieFactsPCA, queryVectPCA, usrMovies)

#3. for LDA
movieFactsLDA = mr.formLdaMat(numSemantics)
queryVectLDA, usrMovies = mr.formQueryVect(movieFactsLDA, userId)
rankedResLDA = mr.getSimilarity(movieFactsLDA, queryVectLDA, usrMovies)

#4. for Tensor
movieFactsTens = mr.formTensMat()
queryVectTens, usrMovies = mr.formQueryVect(movieFactsTens, userId)
rankedResTens = mr.getSimilarity(movieFactsTens, queryVectTens, usrMovies)

#5. for Pers Page Rank
matPPR = mr.formPPRMatrix()
matrix = np.matmul(matPPR,np.transpose(matPPR))
#query, usrMovies = mr.formQueryVect(matPPR, userId)
rankedResPPR = mr.pprRes(matrix, usrMovies)

#print(rankedResSVD)
#print(rankedResPCA)
#print(rankedResLDA)
#print(rankedResTens)
#print(rankedResPPR)

rankedRes = mr.rankCombine(rankedResSVD,rankedResPCA,rankedResLDA,rankedResTens,rankedResPPR,usrMovies)
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])

relMoviesIdx = input("Relavent Movies = ").split(',')
irrMoviesIdx = input("Irrelavent Movies = ").split(',')
seeds = mr.formNewSeeds(usrMovies, rankedRes, relMoviesIdx)
#print("seeds = ", seeds,usrMovies)
relMoviesIdx, irrMoviesIdx, irrMovies = mr.getRelIrrMov(rankedRes, relMoviesIdx, irrMoviesIdx)

if(len(relMoviesIdx) == 0 and len(irrMoviesIdx) == 0):
	print("\nNo feedback provided. The revised movies will be the same as the previous recommended movies\n")
else:
	usrMovies.extend(irrMovies)
	rankedResSVD = pf.getRevisedRanks(movieFactsSVD, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVectSVD)
	rankedResPCA = pf.getRevisedRanks(movieFactsPCA, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVectPCA)
	rankedResLDA = pf.getRevisedRanks(movieFactsLDA, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVectLDA)
	rankedResTens = pf.getRevisedRanks(movieFactsTens, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVectTens)
	rankedResPPR = pf.getRevisedRanksPPR(matPPR, seeds, relMoviesIdx, irrMoviesIdx, movies, usrMovies)
	rankedRes = mr.rankCombine(rankedResSVD,rankedResPCA,rankedResLDA,rankedResTens,rankedResPPR,usrMovies)
	print("Revised Results:")
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])
