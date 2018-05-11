# Run this file only once to transfer data from csv file to Database
import csv
import dbInfo as di
import sqlite3

myDbConn = sqlite3.connect('mwdproj.db')
myDbCurr = myDbConn.cursor()

#Creating the tables below
myDbCurr.execute("create table if not exists genome_tags(tag_id text, tag text)")
myDbCurr.execute("create table if not exists imdb_actor_info(actor_id text, name text, gender text, tags text)")
myDbCurr.execute("create table if not exists mlmovies(movie_id text, genre text)")
myDbCurr.execute("create table if not exists mlratings(movie_id text, user_id text, imdb_id text, rating integer, timestamp text)")
myDbCurr.execute("create table if not exists mltags(user_id text, movie_id text, tag_id text, timestamp text)")
myDbCurr.execute("create table if not exists mlusers(user_id text, tags text)")
myDbCurr.execute("create table if not exists movie_actor(movie_id text, actor_id text, actor_movie_rank integer)")
myDbCurr.execute("create table if not exists movie_info(movie_id text, movie_name text, year integer, tags text, avg_ratings real)")
myDbCurr.execute("create table if not exists genre_info(genre text, tags text)")

#Insert values into the genome_tags
with open('../testdata/genome-tags.csv', encoding='utf8') as genome_tags:
	entries = csv.DictReader(genome_tags)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into genome_tags values(?,?)",[entry['tagId'],entry['tag']])
	
with open('../testdata/imdb-actor-info.csv', encoding='utf8') as imdb_actor_info:
	entries = csv.DictReader(imdb_actor_info)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into imdb_actor_info values(?,?,?,?)",[entry['id'],entry['name'],entry['gender'],''])

with open('../testdata/mlmovies.csv', encoding='utf8') as mlmovies:
	entries = csv.DictReader(mlmovies)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into movie_info values(?,?,?,?,?)",[entry['movieid'],entry['moviename'], entry['year'], '', 0.0])

with open('../testdata/mlmovies.csv', encoding='utf8') as mlmovies:
	entries = csv.DictReader(mlmovies)
	for entry in entries:
		#print(entry)
		genres = entry['genres'].split("|")
		for genre in genres:
			myDbCurr.execute("insert into mlmovies values(?,?)",[entry['movieid'],genre])

with open('../testdata/mlratings.csv', encoding='utf8') as mlratings:
	entries = csv.DictReader(mlratings)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into mlratings values(?,?,?,?,?)",[entry['movieid'],entry['userid'],entry['imdbid'],entry['rating'],entry['timestamp']])

with open('../testdata/mltags.csv', encoding='utf8') as mltags:
	entries = csv.DictReader(mltags)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into mltags values(?,?,?,?)",[entry['userid'],entry['movieid'],entry['tagid'],entry['timestamp']])

with open('../testdata/mlusers.csv', encoding='utf8') as mlusers:
	entries = csv.DictReader(mlusers)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into mlusers values(?,?)",[entry['userid'], ''])

with open('../testdata/movie-actor.csv', encoding='utf8') as movie_actor:
	entries = csv.DictReader(movie_actor)
	for entry in entries:
		#print(entry)
		myDbCurr.execute("insert into movie_actor values(?,?,?)",[entry['movieid'],entry['actorid'],entry['actor_movie_rank']])

myDbConn.commit()
print("6")
# Add tags to actors
actors = di.getAllActors()
for actor in actors:
	movies = di.getActorMovies(actor[0])
	tags = ''
	for movie in movies:
		movieTags = di.getMovieTags(movie[0])
		for movieTag in movieTags:
			if(tags == ''):
				tags = movieTag[0]
			elif(movieTag[0] not in tags):
				tags = tags + ',' + movieTag[0]
	myDbCurr.execute("update imdb_actor_info set tags = ? where actor_id = ?",(tags, actor[0]))
myDbConn.commit()
print("5")
# Add tags to Genres
myDbCurr.execute("select distinct genre from mlmovies")
genres = myDbCurr.fetchall()
for genre in genres:
	movies = di.getGenreMovies(genre[0])
	tags = ''
	for movie in movies:
		movieTags = di.getMovieTags(movie[0])
		for movieTag in movieTags:
			if(tags == ''):
				tags = movieTag[0]
			elif(movieTag[0] not in tags):
				tags = tags + ',' + movieTag[0]
	myDbCurr.execute("insert into genre_info values(?,?)",[genre[0], tags])
myDbConn.commit()
print("4")
'''
# Add tags to Users
users = di.getAllUsers()
for user in users:
	movies = di.getUserMovies(user[0])
	tags = ''
	for movie in movies:
		movieTags = di.getMovieTags(movie[0])
		for movieTag in movieTags:
			if(tags == ''):
				tags = movieTag[0]
			elif(movieTag[0] not in tags):
				tags = tags + ',' + movieTag[0]
	myDbCurr.execute("update mlusers set tags = ? where user_id = ?", (tags, user[0]))
myDbConn.commit()
'''
print("3")
movies = di.getAllMovies()
# Add tags to Movies
for movie in movies:
	movieTags = di.getMovieTags(movie[0])
	tags = ''
	for movieTag in movieTags:
		if(tags == ''):
			tags = movieTag[0]
		elif(movieTag[0] not in tags):
			tags = tags + ',' + movieTag[0]
	myDbCurr.execute("update movie_info set tags = ? where movie_id = ?",(tags, movie[0]))
myDbConn.commit()
print("2")
'''
# Add average ratings to movies
for movie in movies:
	movieRtngs = di.getMovieRtngs(movie[0])
	numOfRtngs = len(movieRtngs)
	totalRtng = 0
	for rating in movieRtngs:
		totalRtng = totalRtng + rating[0]
	if(numOfRtngs == 0):
		avgRtng = 0
	else:
		avgRtng = totalRtng/numOfRtngs
	#print("mv rates",movie[0],avgRtng)
	myDbCurr.execute("update movie_info set avg_ratings = ? where movie_id = ?",(avgRtng, movie[0]))
myDbConn.commit()
'''

print("1")
myDbCurr.execute("select count(*) from movie_actor")
print(myDbCurr.fetchone())
myDbCurr.execute("select count(*) from mlusers")
print(myDbCurr.fetchone())
myDbCurr.execute("select count(*) from mltags")
print(myDbCurr.fetchone())
myDbCurr.execute("select count(*) from mlratings")
print(myDbCurr.fetchone())
myDbCurr.execute("select count(*) from mlmovies")
print(myDbCurr.fetchone())
myDbCurr.execute("select count(*) from imdb_actor_info")
print(myDbCurr.fetchone())
myDbConn.close()
