import numpy as np
import utils
import persPageRank as ppr
import dbInfo as db
import similarity
#np.set_printoptions(threshold=np.nan)

actTags = similarity.getActorTagMatrix()
sim = np.matmul(actTags,np.transpose(actTags))
print("\n\nActor-Actor similarity matrix:\n", sim, "\n\nsize of matrix :", sim.shape)
seeds = input("\nGive Seed Actors: ").split(",")
actorNames = db.getAllActorNames()
actorIds = db.getAllActors()
seedNames = []
for i in range(len(actorIds)):
	if(actorIds[i][0] in seeds):
		seedNames.append(actorNames[i][0])
seedMat = ppr.formSeed(seeds, actorIds)
pprOut = ppr.personalizedPageRank(sim, seedMat, 0.85)
print("\n\n10 most related actors:\n")
for act in ppr.rankedList(pprOut, actorNames, seedNames, 10):
	print(act)
