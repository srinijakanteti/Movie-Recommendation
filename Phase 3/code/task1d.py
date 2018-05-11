import dbInfo as di
import tfIdfCalc as idf
import utils
from scipy.spatial import distance

def movieTagSpace(movieId):
	tagIds = di.getMovieTags(movieId)
	tagLen = len(tagIds)
	actorlist= di.getAllActors()
	actorNames = di.getAllActorNames()
	idfActVector = idf.idfActorTag()
	mov = di.getMovieActorIds(movieId)
	movieActors = [0 for i in range(len(mov))]
	for i in range(len(mov)):
		movieActors[i] = mov[i][0]
	mat=[[0 for i in range(tagLen)] for j in range(len(movieActors))]
	newMat=[[0 for i in range(tagLen)] for j in range(len(actorlist))]
	for i in range(len(movieActors)):
		taglist=idf.tfIdfActorTag(movieActors[i], idfActVector)
		for j in range(tagLen):
			if(tagIds[j][0] in taglist.keys()):
				mat[i][j]=taglist[tagIds[j][0]]
	for i in range(0,len(actorlist)):
		if(actorlist[i][0] not in movieActors):
			taglist=idf.tfIdfActorTag(actorlist[i][0], idfActVector)
			for j in range(tagLen):
				if(tagIds[j][0] in taglist.keys()):
					newMat[i][j]=taglist[tagIds[j][0]]
	actVect=[0 for i in range(tagLen)] 
	for j in range(len(movieActors)):
		for i in range(tagLen):
			actVect[i] = actVect[i]+ mat[j][i]
	dist = {}
	for i in range(len(newMat)):
		if(actorlist[i][0] not in movieActors):
			dist[actorNames[i][0]] = distance.euclidean(newMat[i],actVect)
	return utils.sortByValue(dist)[-10:]

movieId = input('\nEnter the movie id: ')
actors = movieTagSpace(movieId)
print("\n10 related actors not in the given movie are:\n")
for act in reversed(actors):
	print(act)