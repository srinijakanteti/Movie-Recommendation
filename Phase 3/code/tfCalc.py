import sqlite3
import utils
import dbInfo as di
from Movie import Movie
from Actor import Actor
from Genre import Genre
from User import User

def tfActorTag(actorId):
	movies = di.getActorMovies(actorId)
	#print(movies)
	actor = Actor(actorId)
	for movie in movies:
		# Here the first element in the entry is movieId and second is the actor rank
		movieId = movie[0]
		rank = movie[1]
		# Create the Movie obj and add to the Actor
		mv = Movie(movieId, rank)
		# Get the tags of movie
		movieTags = di.getMovieTags(movieId)
		#print(movieId)
		#print(movieTags)
		# Calculate the weight of the tags
		for movieTag in movieTags:
			tagId = movieTag[0]
			timeStamp = movieTag[1]
			mv.addTag(tagId, timeStamp)
		actor.addMovie(mv)
	tfVector = {}
	actor.setUnqTags()
	unqTags = actor.getUnqTags()
	for tagId in unqTags:
		tfFactorTag = 0
		#print("tagId "+tagId)
		for movie in actor.getMovies():
			searchTags = movie.getTags()
			tfFactor = 0
			totalMovieWeight = 0
			movRankWeight = movie.getRWeight()
			#print(movRankWeight)
			for tag in searchTags:
				#print(tag.getId())
				if(tag.getId() == tagId):
					tfFactor = tfFactor + tag.getTimeWeight()
				totalMovieWeight = totalMovieWeight + 1
			#print(tfFactor)
			#print(totalMovieWeight)
			if(totalMovieWeight != 0): # Check this condition because their are movies with no tags
				tfFactorTag = tfFactorTag + (movRankWeight*tfFactor)/totalMovieWeight
		tfVector[tagId] = tfFactorTag
	tfVector = utils.sortByValue(tfVector)
	return utils.normalizeVector(tfVector)
	
def tfGenreTag(genre):
	genObj = createGenObj(genre)
	unqTags = genObj.getUnqTags()
	tfVector = {}
	#print(unqTags)
	for tagId in unqTags:
		tfFactorTag = 0
		for movie in genObj.getMovies():
			searchTags = movie.getTags()
			tfFactor = 0
			totalMovieWeight = 0
			for tag in searchTags:
				if(tag.getId() == tagId):
					tfFactor = tfFactor + tag.getTimeWeight()
					#print(tfFactor)
				totalMovieWeight = totalMovieWeight + 1
			if(totalMovieWeight != 0):
				tfFactorTag = tfFactorTag + tfFactor/totalMovieWeight
		tfVector[tagId] = tfFactorTag
	tfVector = utils.sortByValue(tfVector)
	return utils.normalizeVector(tfVector)
	
def tfUserTag(userId):
	usrObj = User(userId)
	movies = di.getUserMovies(userId)
	for movieId in movies:
		movieId = movieId[0]
		mv = Movie(movieId, 0) # Here the actor movie rank is not reqd., setting this to 0
		movieTags = di.getMovieTags(movieId)
		for movieTag in movieTags:
			tagId = movieTag[0]
			timeStamp = movieTag[1]
			mv.addTag(tagId, timeStamp)
		usrObj.addMovie(mv)
	tfVector = {}
	usrObj.setUnqTags()
	unqTags = usrObj.getUnqTags()
	#print(unqTags)
	for tagId in unqTags:
		tfFactorTag = 0
		for movie in usrObj.getMovies():
			searchTags = movie.getTags()
			tfFactor = 0
			totalMovieWeight = 0
			for tag in searchTags:
				if(tag.getId() == tagId):
					tfFactor = tfFactor + tag.getTimeWeight()
					#print(tfFactor)
				totalMovieWeight = totalMovieWeight + 1
			if(totalMovieWeight != 0):
				tfFactorTag = tfFactorTag + tfFactor/totalMovieWeight
		tfVector[tagId] = tfFactorTag
	tfVector = utils.sortByValue(tfVector)
	return utils.normalizeVector(tfVector)

def createGenObj(genre):
	genObj = Genre(genre)
	movies = di.getGenreMovies(genre)
	for movieId in movies:
		movieId = movieId[0]
		mv = Movie(movieId, 0) # Here the actor movie rank is not reqd., setting this to 0
		movieTags = di.getMovieTags(movieId)
		#print("tags are")
		#print(movieTags)
		for movieTag in movieTags:
			tagId = movieTag[0]
			timeStamp = movieTag[1]
			mv.addTag(tagId, timeStamp)
		genObj.addMovie(mv)
		#print("mv unq tags are")
		#print(mv.getUnqTags())
	genObj.setUnqTags()
	return genObj

def tfMovTag(movieId):
	mv = Movie(movieId, 0) # Here the actor movie rank is not reqd., setting this to 0
	movieTags = di.getMovieTags(movieId)
	#print("tags are")
	#print(movieTags)
	for movieTag in movieTags:
		tagId = movieTag[0]
		timeStamp = movieTag[1]
		mv.addTag(tagId, timeStamp)
	tfArray = utils.getGenreMovieTags(mv)
	return tfArray

#print(tfMovTag('3854'))