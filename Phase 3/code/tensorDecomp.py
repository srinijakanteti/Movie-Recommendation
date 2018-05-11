import dbInfo as di
from collections import defaultdict
import numpy as np
import tensorly as tl
tl.set_backend('numpy')
from tensorly.decomposition import parafac, non_negative_parafac
from scipy.cluster.vq import kmeans2, whiten

# This returns data reqd. for the Actor-Movie-Year tensor in vector form
def vectActMovYr():
	actors = di.getAllActors()
	movies = di.getAllMovies()
	years = di.getAllYears()
	movYearsArray = di.getAllMovieYrs()
	movYears = {}
	for arr in movYearsArray:
		movYears[arr[0]] = arr[1]
	#print("movYears", movYears)
	actMoviesDb = {}
	moviesArr = []
	for mov in movies:
		moviesArr.append(mov[0])
	for act in actors:
		actMovies = di.getActorMovieIds(act[0])
		actMov= []
		chk = 0
		for mov in actMovies:
			actMov.append(mov[0])
			if(mov[0] in moviesArr):
				chk = 1
		if(chk == 1):
			actMoviesDb[act[0]] = actMov
	print("\ngot the actor movies\n")
	vect = defaultdict(lambda :defaultdict(dict))
	for act in actMoviesDb:
		#print("movie set", act)
		for mov in moviesArr:
			#print("mov",mov)
			for yr in years:
				#print("yr",yr[0])
				vect[act][mov][yr[0]] = 0
				# Set the value to 1 if the given cond. is satisfied
				if((mov in actMoviesDb[act]) and (movYears[mov] == yr[0])):
					vect[act][mov][yr[0]] = 1
	#print(vect['1'])
	return (vect, actors, movies, years)

# This returns the data reqd. for the Tag-Movie-Rating tensor in vector form
def vectTagMovRat():
	tags = di.getAllTags()
	movies = di.getAllMovies()
	ratings = di.getAllRatings()
	avgRatingsArray = di.getAllMovieRtngs()
	avgRatings = {}
	for arr in avgRatingsArray:
		avgRatings[arr[0]] = arr[1]
	#print("avgRatings",avgRatings)
	vect = defaultdict(lambda :defaultdict(dict))
	for mov in movies:
		movTags = di.getMovieTagIds(mov[0])[0][0].split(",")
		for tag in tags:
			for rtng in ratings:
				vect[tag[0]][mov[0]][rtng[0]] = 0
				# Set the value to 1 if the given cond. is satisfied
				if((tag[0] in movTags) and (rtng[0] <= avgRatings[mov[0]])):
					vect[tag[0]][mov[0]][rtng[0]] = 1
	#print(vect['1'])
	return (vect, tags, movies, ratings)

# This returns data reqd. for the Actor-Movie-Year tensor in vector form
def vectActMovTag():
	actors = di.getAllActors()
	tags = di.getAllTags()
	movies = di.getAllMovies()
	years = di.getAllYears()
	movYearsArray = di.getAllMovieYrs()
	movYears = {}
	for arr in movYearsArray:
		movYears[arr[0]] = arr[1]
	#print("movYears", movYears)
	actMoviesDb = {}
	for act in actors:
		actMovies = di.getActorMovieIds(act[0])
		actMov= []
		for mov in actMovies:
			actMov.append(mov[0])
		actMoviesDb[act[0]] = actMov
	vect = defaultdict(lambda :defaultdict(dict))
	for mov in movies:
		movTags = di.getMovieTagIds(mov[0])[0][0].split(",")
		#print(len(movTags))
		for act in actors:
			actMovies = actMoviesDb[act[0]]
			#print("actMovies:",actMovies)
			for tag in tags:
				#print("tag",tag[0])
				vect[mov[0]][act[0]][tag[0]] = 0
				#print("i am here")
				# Set the value to 1 if the given cond. is satisfied
				if((mov[0] in actMovies) and (tag[0] in movTags)): #and (movYears[mov[0]] == yr[0])):
					vect[act[0]][mov[0]][tag[0]] = movYears[mov[0]]
	#print(vect['1'])
	return (vect, actors, movies, years)

#This func returns the tensor form of the given dict/vector along with its dimensions
def vectToTens(vect):
	dimA = len(vect)
	for v in vect:
		dimB = len(vect[v])
		for t in vect[v]:
			dimC = len(vect[v][t])
			break
		break
	#print(dimA,dimB,dimC)
	arr = np.zeros((dimA,dimB,dimC))
	i = 0
	for a in vect:
		j = 0
		for b in vect[a]:
			k = 0
			for c in vect[a][b]:
				arr[i][j][k] = vect[a][b][c]
				k += 1
			j += 1
		i += 1
	tens = tl.tensor(arr)
	#print(len(tens[0][0]))
	return tens

def tensDecomp(tens,rnk):
	# Make this check as we need to reduce the number of dimensions and not increase it
	if(rnk >= len(tens[0][0])):
		print("Error in data: rank is greater than number of features")
		return
	#factors = parafac(tens, rnk)
	factors = non_negative_parafac(tens, rnk)
	#print(factors[0])
	return factors
