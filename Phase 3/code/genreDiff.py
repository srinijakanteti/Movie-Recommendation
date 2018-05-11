import utils
import dbInfo as di
from Genre import Genre
import tfCalc as tf
import sqlite3

myDbConn = sqlite3.connect('mwdproj.db')
myDbCurr = myDbConn.cursor()

def differGenre(g1,g2,model):
	if(model == 'tf-idf-diff'):
		return(tfIdfDiff(g1,g2))
	elif(model == 'p-diff1'):
		return(pDiff1(g1,g2))
	else:
		return(pDiff2(g1,g2))

def tfIdfDiff(g1,g2):
	tfG1 = tf.tfGenreTag(g1)
	tfG2 = tf.tfGenreTag(g2)
	totalGenres = [g1,g2]
	
	tagsG1G2 = tfG1.keys() + tfG2.keys()
	unqtagsG1G2 = []
	#Get the union of tags in g1 and g2
	for tag in tagsG1G2:
		if(tag not in unqtagsG1G2):
			unqtagsG1G2.append(tag)
	genreCount = 2
	idf = {}
	tfidf = {}
	for tag in unqtagsG1G2:
		idf[tag] = 0
		for genre in totalGenres:
			tagchk = 0
			movies = di.getGenreMovies(genre)
			for mov in movies:
				mov = mov[0]
				myDbCurr.execute("select tag_id from mltags where movie_id = ?", [mov])
				movTags = myDbCurr.fetchall()
				for movTag in movTags:
					if(tag == movTag):
						tagchk = 1
						idf[tag] = idf[tag] + 1
						break
				if(tagchk == 1):
					break
		tfidf[tag] = (math.log(genreCount/idf[tag]))*(tfG1[tag] - tfG2[tag])
	tfidf = utils.sortByValue(tfidf)
	return utils.roundOfValues(tfidf)

def pDiff1(g1,g2):
	objG1 = tf.createGenObj(g1)
	objG2 = tf.createGenObj(g2)
	movG1G2 = objG1.getMovies() + objG2.getMovies()
	unqMovG1G2 = []
	#Get the union of movies in g1 and g2
	for mov in movG1G2:
		if(mov.getId() not in unqMovG1G2):
			unqMovG1G2.append(mov)
	R = len(objG1.getMovies())
	M = len(unqMovG1G2)
	diffVect = {}
	for tagG1 in objG1.getUnqTags():
		r = 0
		m = 0
		for mov in objG1.getMovies():
			tagChk = 0
			unqTags = mov.getUnqTags()
			for tag in unqTags:
				if(tag == tagG1):
					tagChk = 1
			if(tagChk == 1):
				r = r + 1
		for mov in unqMovG1G2:
			tagChk = 0
			unqTags = mov.getUnqTags()
			for tag in unqTags:
				if(tag == tagG1):
					tagChk = 1
			if(tagChk == 1):
				m = m + 1
		x = (r/(R-r))/((m-r)/(M-m-R+r))
		y = abs((r/R)-((m-r)/(M-R)))
		diffVect[tagG1] = (math.log10(x))*y
	return diffVect

def pDiff2(g1,g2):
	objG1 = tf.createGenObj(g1)
	objG2 = tf.createGenObj(g2)
	movG1G2 = objG1.getMovies() + objG2.getMovies()
	unqMovG1G2 = []
	#Get the union of movies in g1 and g2
	for mov in movG1G2:
		if(mov.getId() not in unqMovG1G2):
			unqMovG1G2.append(mov)
	R = len(objG2.getMovies())
	M = len(unqMovG1G2)
	print(R,M)
	diffVect = {}
	for tagG1 in objG1.getUnqTags():
		r = 0
		m = 0
		for mov in objG2.getMovies():
			tagChk = 0
			unqTags = mov.getUnqTags()
			for tag in unqTags:
				if(tag == tagG1):
					tagChk = 1
			if(tagChk == 0):
				r = r + 1
		for mov in unqMovG1G2:
			tagChk = 0
			unqTags = mov.getUnqTags()
			for tag in unqTags:
				if(tag == tagG1):
					tagChk = 1
			if(tagChk == 0):
				m = m + 1
		print(m)
		x = (r/(R-r))/((m-r)/(M-m-R+r))
		y = abs((r/R) - ((m-r)/M-R))
		diffVect[tagG1] = (math.log10(x))*y
	return diffVect
myDbConn.close()