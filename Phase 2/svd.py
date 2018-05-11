import sqlite3
import utils
import dbInfo as db
from Movie import Movie
from Actor import Actor
from Genre import Genre
from User import User
import tfCalc as tf
import re
import numpy as np
import genreMovieTags as genmov

def genSVDMatrix(genrelist):
		#genrelist = db.getGenres()
		#genrelist = "Action"
		h = 92;
		
		genObj = tf.createGenObj(genrelist)
		movies = genObj.getMovies()
		Matrix = [[0 for x in range(0,h)]for y in range(0,len(movies))]
		movVects = {}
		i=0;
		#temp=genmov.getGenreMovieTags(genrelist)
		for movie in movies:
			temp=genmov.getGenreMovieTags(movie)
			#temp=tf.tfGenreTag(''.join(genrelist[i]))
			#temp=tf.tfGenreTag(genrelist)
			#for j in temp.keys():
			Matrix[i]=temp
			i=i+1
		return Matrix

def Calcsvd(A):
	U, s, V = np.linalg.svd(A, full_matrices=True)
	print(U)
	print(s)
	print(V)

