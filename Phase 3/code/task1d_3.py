import dbInfo as di
import probFeedback as pf
import movieRecomm as mr
import numpy as np

userId = input("\nGive User Id: ")
numMovies = 5

movies = di.getAllMovies()
movieNames = di.getAllMovieNames()
moviesArr = []
for mov in movies:
	moviesArr.append(mov[0])

mat = mr.formPPRMatrix()
matrix = np.matmul(mat,np.transpose(mat))

usrSeenMovies = di.getusrMovTime(userId)
if(len(usrSeenMovies) <= 0):
	print("user has not watched any movies to give suggestions")
	sys.exit()
usrMovies = []
for mov in usrSeenMovies:
	usrMovies.append(mov[0])
print("\nseeds =", usrMovies)
rankedRes = mr.pprRes(matrix, usrMovies)
#print("ranked res",rankedRes)
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
	print("\nNo feedback provided. The revised movies will be the same as the previous recommended movies")
else:
	print("\nnew seeds =",seeds)
	usrMovies.extend(irrMovies)
	rankedRes = pf.getRevisedRanksPPR(mat, seeds, relMoviesIdx, irrMoviesIdx, movies, usrMovies)
	print("\nRevised Results:")
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])
