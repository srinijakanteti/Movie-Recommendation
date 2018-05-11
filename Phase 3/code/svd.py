import dbInfo as db
import numpy as np
import utils
import tfCalc as tf
import warnings
warnings.filterwarnings("ignore")

allTags = db.getAllTags()
lenTags = len(allTags)
#this function will generate a Matrix to be used as input to SVD
def genSVDMatrix(genrelist):
	genObj = tf.createGenObj(genrelist)
	movies = genObj.getMovies()
	matrix = [[0 for x in range(0,lenTags)]for y in range(0,len(movies))]
	i=0
	for movie in movies:
		matrix[i] = utils.getGenreMovieTags(movie)
		i += 1
	return matrix

def svdCalc(mat,numSem):
	U, s, V = np.linalg.svd(mat, full_matrices=False)
	sem = np.zeros((numSem,len(V[0])))
	for i in range(numSem):
		for j in range(len(V[0])):
			sem[i][j] = V[i][j]
	return sem

def svdUout(mat,numSem):
	U, s, V = np.linalg.svd(mat, full_matrices=False)
	print(U.shape)
	sem = np.zeros((len(U),numSem))
	for i in range(len(U)):
		for j in range(numSem):
			sem[i][j] = U[i][j]
	return sem