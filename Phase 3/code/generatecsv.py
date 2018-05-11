import numpy
import tfIdfCalc as idf
import probFeedback as pf
import tfCalc as tf
import dbInfo as di
import random
import dbInfo as db

movies = di.getAllMovies()

mat = [['' for i in range(2)] for j in range(len(movies))]
#mat = numpy.zeros((len(mvies),2))
labels = ['0', '1','2']
ch = []
for i in range(len(movies)):
	mat[i][0] = movies[i][0]
	#mat[i][1] = db.getMovieGenre(movies[i][0])[0]
	mat[i][1] = random.choice(labels)

numpy.savetxt('foo.csv', mat, fmt='%s',delimiter = ',') 