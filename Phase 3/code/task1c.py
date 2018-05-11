import dbInfo as di
import tfIdfCalc as idf
import numpy as np
import utils
import similarity
from scipy.spatial import distance

actorTags = similarity.getActorTagMatrix()
actorList = di.getAllActors()
actorNames = di.getAllActorNames()

def simActors(actId):
	for i in range(len(actorTags)):
		if(actId == actorList[i][0]):
			givenActor = actorTags[i]
	d = {}
	for i in range(len(actorList)):
		if(actId != actorList[i][0]):
			d[actorNames[i][0]] = distance.euclidean(givenActor,actorTags[i])
	return utils.sortByValue(d)[-10:]

def simActors2(actId):
	numSemantics = 5
	u,s,v = np.linalg.svd(actorTags,0)
	x=np.zeros((len(u),numSemantics))
	givenActor = np.zeros(numSemantics)
	for i in range(len(u)):
		for j in range(numSemantics):
			if(actId == actorList[i][0]):
				givenActor[j] = u[i][j]
			x[i][j] = u[i][j]
	d = {}
	for i in range(len(actorList)):
		if(actId != actorList[i][0]):
			d[actorNames[i][0]] = distance.euclidean(givenActor,x[i])
	return utils.sortByValue(d)[-10:]

actId = input('Actor Id: ')
print("\n10 similar actors Using tf-IDF tags:\n")
for act in reversed(simActors(actId)):
	print(act)
print("\n\n10 similar actors Using SVD:\n")
for act in reversed(simActors2(actId)):
	print(act)