import dbInfo as di
import probFeedback as pf
import movieRecomm as mr

numMovies = 5

movies = di.getAllMovies()
movieNames = di.getAllMovieNames()
userId = input("\nGive User Id: ")

moviesArr = []
for mov in movies:
	moviesArr.append(mov[0])

movieFacts = mr.formTensMat()
queryVect, usrMovies = mr.formQueryVect(movieFacts, userId)
rankedRes = mr.getSimilarity(movieFacts, queryVect, usrMovies)
#print("ranked res",rankedRes)
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])

relMoviesIdx = input("Relavent Movies = ").split(',')
irrMoviesIdx = input("Irrelavent Movies = ").split(',')
relMoviesIdx, irrMoviesIdx, irrMovies = mr.getRelIrrMov(rankedRes, relMoviesIdx, irrMoviesIdx)
if(len(relMoviesIdx) == 0 and len(irrMoviesIdx) == 0):
	print("\nNo feedback provided. The revised movies will be the same as the previous recommended movies\n")
else:
	usrMovies.extend(irrMovies)
	rankedRes = pf.getRevisedRanks(movieFacts, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVect)
	print("\nRevised Results:")
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])
