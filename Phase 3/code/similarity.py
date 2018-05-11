import dbInfo as di
import tfIdfCalc as idf
import numpy as np

def getActorTagMatrix():
	tagIds = di.getAllTags()
	tagLen = len(tagIds)
	actorNames = di.getAllActorNames()
	actorlist = di.getAllActors()
	actorTags = np.zeros((len(actorlist),tagLen))
	i=0
	idfActVector = idf.idfActorTag()
	for actor in actorlist:
		actVect = idf.tfIdfActorTag(actor[0], idfActVector)
		for j in range(tagLen):
			if(tagIds[j][0] in actVect.keys()):
				actorTags[i][j]=actVect[tagIds[j][0]]
		i += 1
	return actorTags

def getCoactorMatrix():
	actorList = di.getAllActors()
	actLen = len(actorList)
	sim = np.zeros((actLen,actLen))
	actMovies = [0 for i in range(actLen)]
	for i in range(actLen):
		actMovies[i] = di.getActorMovieIds(actorList[i][0])
	for i in range(actLen):
		for j in range(actLen):
			set1 = set(actMovies[i])
			set2 = set(actMovies[j])
			sim[i][j]=len(set1&set2)
	return sim