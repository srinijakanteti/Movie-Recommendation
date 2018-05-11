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

Mat = genSVDMatrix(input('Enter the Genre: '))
Mat_Transpose = Mat.transpose()

for i in range(len(Mat)):
   # iterate through columns of Y
   for j in range(len(Mat_Transpose[0])):
       # iterate through rows of Y
       for k in range(len(Mat_Transpose)):
           Output_Matrix[i][j] += Mat[i][k] * Mat_Transpose[k][j]

for r in Output_Matrix:
   print(r)
   
pca = PCA(n_components=2)
pca.fit(Output_Matrix)
print(pca.explained_variance_ratio_)  
print(pca.singular_values_)
	

