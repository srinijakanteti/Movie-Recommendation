import dbInfo as di
import probFeedback as pf
import movieRecomm as mr

numSemantics = 20
numMovies = 5
userId = input("\nGive User Id: ")

movies = di.getAllMovies()
moviesArr = []
movieNames = di.getAllMovieNames()
for mov in movies:
	moviesArr.append(mov[0])

choice = input("select:\n1:\tsvd\n2:\tpca\n")

if(choice == '1'):
	print("\nSVD selected")
	movieFacts = mr.formSvdMat(numSemantics)
else:
	print("\nPCA selected")
	movieFacts = mr.formPcaMat(numSemantics)
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
#print("rel irr mov = ",relMoviesIdx, irrMoviesIdx)
if(len(relMoviesIdx) == 0 and len(irrMoviesIdx) == 0):
	print("\nNo feedback provided. The revised movies will be the same as the previous recommended movies\n")
else:
	#print(irrMovies,usrMovies)
	usrMovies.extend(irrMovies)
	#print(usrMovies)
	rankedRes = pf.getRevisedRanks(movieFacts, relMoviesIdx, irrMoviesIdx, movies, usrMovies, queryVect)
	print("\nRevised Results:")
print("\nRank\tMovie Id\tMovie Name\n")
for i in range(numMovies):
	movIdx = moviesArr.index(rankedRes[i])
	print(i+1,":\t",rankedRes[i],"\t\t",movieNames[movIdx][0])
