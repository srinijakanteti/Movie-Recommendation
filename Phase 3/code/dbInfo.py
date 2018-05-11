#This module gets the required information from the database
#This also does the updates required to be done to the DB after initial assignment
import sqlite3

myDbConn = sqlite3.connect('mwdproj_tens.db')
myDbCurr = myDbConn.cursor()

#Get all the movies and movie_actor_rank of an actor worked in
def getActorMovies(actorId):
	myDbCurr.execute("select movie_id,actor_movie_rank from movie_actor where actor_id = ?", [actorId])
	return myDbCurr.fetchall()

# Get tag_ids of a movie
def getActorMovieIds(actorId):
	myDbCurr.execute("select movie_id from movie_actor where actor_id = ?", [actorId])
	return myDbCurr.fetchall()

# This returns all tag info related to a movie
def getMovieTags(movieId):
	myDbCurr.execute("select tag_id,timestamp from mltags where movie_id = ?", [movieId])
	return myDbCurr.fetchall()

# Get tag_ids of a movie
def getMovieTagIds(movieId):
	myDbCurr.execute("select tags from movie_info where movie_id = ?", [movieId])
	return myDbCurr.fetchall()

def getGenreMovies(genre):
	myDbCurr.execute("select movie_id from mlmovies where genre = ?", [genre])
	return myDbCurr.fetchall()

def getUserMovies(userId):
	myDbCurr.execute("select movie_id from mltags where user_id = ?", [userId])
	return myDbCurr.fetchall()

def getAllActors():
	myDbCurr.execute("select actor_id from imdb_actor_info")
	return myDbCurr.fetchall()

def getAllGenres():
	myDbCurr.execute("select genre from genre_info")
	return myDbCurr.fetchall()

def getAllUsers():
	myDbCurr.execute("select user_id from mlusers")
	return myDbCurr.fetchall()

def getAllTags():
	myDbCurr.execute("select tag_id from genome_tags")
	return myDbCurr.fetchall()

def getAllTagNames():
	myDbCurr.execute("select tag from genome_tags")
	return myDbCurr.fetchall()

def getAllMovies():
	myDbCurr.execute("select movie_id, year from movie_info")
	return myDbCurr.fetchall()

def getAllMovieNames():
	myDbCurr.execute("select movie_name from movie_info")
	return myDbCurr.fetchall()

def getAllYears():
	myDbCurr.execute("select distinct year from movie_info")
	return myDbCurr.fetchall()

def getAllRatings():
	myDbCurr.execute("select distinct rating from mlratings")
	rates = myDbCurr.fetchall()
	rates.append((0,))
	return rates

def getAllMovieYrs():
	myDbCurr.execute("select movie_id, year from movie_info")
	return myDbCurr.fetchall()

# This returns all the ratings of given movie 
def getMovieRtngs(movieId):
	myDbCurr.execute("select rating from mlratings where movie_id = ?", [movieId])
	return myDbCurr.fetchall()

# This returns average ratings of all the movies
def getAllMovieRtngs():
	print("i am here code may not work")
	myDbCurr.execute("select movie_id, avg_ratings from movie_info")
	return myDbCurr.fetchall()

def getActorTags(actorId):
	myDbCurr.execute("select tags from imdb_actor_info where actor_id = ?", [actorId])
	return myDbCurr.fetchone()

def getGenreTags(genre):
	myDbCurr.execute("select tags from genre_info where genre = ?", [genre])
	return myDbCurr.fetchone()

def getUserTags(userId):
	print("i am here code may not work")
	myDbCurr.execute("select tags from mlusers where user_id = ?", [userId])
	return myDbCurr.fetchone()

def getActorName(actorId):
	myDbCurr.execute("select name from imdb_actor_info where actor_id = ?", [actorId])
	return myDbCurr.fetchone()

def getActId(actor):
	myDbCurr.execute("select actor_id from imdb_actor_info where name = ?", [actorId])
	return myDbCurr.fetchone()
	
def getAllActorNames():
	myDbCurr.execute("select name from imdb_actor_info")
	return myDbCurr.fetchall()

def getUserMoviesRates(userId):
	myDbCurr.execute("select movie_id,rating from mlratings where user_id = ?", [userId])
	return myDbCurr.fetchall()

# Get actor_ids of a movie
def getMovieActorIds(movieId):
    myDbCurr.execute("select actor_id from movie_actor where movie_id = ?", [movieId])
    return myDbCurr.fetchall()
	
def getActorRanks(actorId):
	myDbCurr.execute("select actor_movie_rank from movie_actor where actor_id = ?", [actorId])
	return myDbCurr.fetchall()

def getusrMovTime(userId):
	myDbCurr.execute("select movie_id, timestamp from mlratings where user_id = ?", [userId])
	return myDbCurr.fetchall()

def delRows(table,colName,value):
	query = "delete from "+table+" where "+colName+" = ?"
	myDbCurr.execute(query,[value])
	myDbConn.commit()

def getMLtags():
	myDbCurr.execute("select tag_id from mltags")
	return myDbCurr.fetchall()

def getMvActors():
	myDbCurr.execute("select actor_id from movie_actor")
	return myDbCurr.fetchall()
	
def getMovName(movieId):
	myDbCurr.execute("select movie_name from movie_info where movie_id = ?",[movieId])
	return myDbCurr.fetchall()
