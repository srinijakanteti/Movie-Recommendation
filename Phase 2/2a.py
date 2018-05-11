import sqlite3
import utils
import dbInfo as di
import tfCalc as tc
import numpy as np
from Movie import Movie
from Actor import Actor
from Genre import Genre
from User import User

def formSim(x): #getSimilarityMat is formSim
	if(x == 'actor'): #entity is x
		actors = di.getActors() #actors is actorlist
		actortags = [[0 for i in range(0,92)]for j in range(0,len(actors))]
		i=0
		for actor in actorlist:
			if(actor[0]=='actorid'):
				print("")
			else:
				taglist=tf.tfActorTag(actor[0])

				for j in taglist.keys():
					actortags[i][int(j)]=taglist[j]
				i=i+1
		a=np.array(actortags)
		b=a.transpose()
		c=np.matmul(a,b)
		return c

def PersonalizedPageRank(matrix,seed):
	a=0.85
	seedlist = seed.split(",");
	Normseed = [float(1/len(seedlist)) for i in range(0,matrix.shape[0])]
	inverse = np.linalg.inv(np.identity(matrix.shape[0]) -a*matrix)
	
	for i in seedlist:
		Normseed[int(i)]=(1-a)*float(1/len(seedlist))
	prob = np.matmul(inverse,Normseed)
	return prob

def CoactorSimilarity(entity):
	if(entity=='coactor'):
		actorlist = db.getActors()
		sim=[[0 for i in range(0,len(actorlist))]for j in range(0,len(actorlist))]
		for i in range(1,len(actorlist)):
			for j in range(1,len(actorlist)):
					set1= db.getActorMovieIds(actorlist[i][0])
					set2=db.getActorMovieIds(actorlist[j][0])
					sim[i][j]=len(set(set1)&set(set2))

		print(sim[9])