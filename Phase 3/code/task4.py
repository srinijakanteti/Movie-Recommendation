import dbInfo as db
import numpy as np
import persPageRank as ppr

userId = input("\nGive User Id: ")

movies = db.getAllMovies()
movieNames = db.getAllMovieNames()
tfmovies = {}
for movieId in movies:
	Taglist = db.getMovieTags(movieId[0])
	UnqTags = db.getMovieTagIds(movieId[0])[0][0].split(",")
	#print(UnqTags,movieId,Taglist)
	tfvect = {}
	for tag in UnqTags:
		tffact = 0
		for t in Taglist:
			if(t[0] == tag):
				tffact += 1
		tfvect[tag[0]] = tffact/len(Taglist)
	tfmovies[movieId[0]] = tfvect
tagids = db.getAllTags()
#print(tagids)
movietf = np.zeros((len(tfmovies),len(tagids)))
for i in range(len(tfmovies)):
	for j in range(len(tagids)):
		if(tagids[j][0] in tfmovies[movies[i][0]].keys()):
			movietf[i][j] = tfmovies[movies[i][0]][tagids[j][0]]
matrix = np.matmul(movietf,np.transpose(movietf))
seedList = db.getUserMoviesRates(userId)
seeds = []
for seed in seedList:
	seeds.append(seed[0])
seedNames = []
for i in range(len(movies)):
	if(movies[i][0] in seeds):
		seedNames.append(movieNames[i][0])
#print("seed names = ", seedNames)
seedMat = ppr.formSeed(seeds, movies)
pprOut = ppr.personalizedPageRank(matrix, seedMat, 0.15)
result = ppr.rankedList(pprOut, movieNames, seedNames, 5)
print("\n5 Recomended Movies:\n\n", result)
