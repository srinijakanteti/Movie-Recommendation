import math
import utils
import numpy as np
import persPageRank as ppr

def getRevisedRanks(semMatrix, rel, irr, objList, usrMovies, queryVect):
	N = len(objList)# Number of movies
	numSemantics = len(semMatrix[0])
	R = len(rel)
	Q = len(irr)
	ranks = {}
	r = np.zeros(numSemantics)
	q = np.zeros(numSemantics)
	n = np.zeros(numSemantics)
	p = np.zeros(numSemantics)
	u = np.zeros(numSemantics)
	#pre-calculating ri values
	for i in rel:
		#print("rel = ",i)
		#print("relevent =",semMatrix[i])
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				r[sem] += 1
	#pre-calculating qi values
	for i in irr:
		#print("irrelevant =", semMatrix[i])
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				q[sem] += 1
	#pre-calculating ni values
	for i in range(N):
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				n[sem] += 1
	#pre-calculating pi and ui values for the formula
	#print("r =",r,R,"\nn =",n,N,"\nq =",q,Q)
	for i in range(len(r)):
		p[i] = (r[i]+n[i]/N)/(R+1)
		u[i] = (q[i]+n[i]/N)/(Q+1)
	pSum = np.sum(p)
	uSum = np.sum(u)
	if(pSum == 0): pSum = 1
	if(uSum == 0): uSum = 1
	p = p/pSum
	u = u/uSum
	print("\np =", p)
	print("\nu =", u)
	for sem in range(numSemantics):
		nr = p[sem] * (1-u[sem])
		dr = u[sem] * (1-p[sem])
		#print(nr,dr)
		if(nr != 0 and dr != 0 and nr != dr):
			sim = math.log(nr/dr)
		else:
			sim = 1
		queryVect[sem] = sim * queryVect[sem]
	print("\nNew Query Vector:")
	utils.printVect(queryVect)
	for i in range(N):
		if(objList[i][0] not in usrMovies):
			ranks[objList[i][0]] = np.dot(queryVect,semMatrix[i])
	revisedRanks = utils.sortByValue(ranks)
	ranks = []
	for r in revisedRanks:
		ranks.append(r[0])
	#print(revisedRanks)
	return ranks

def getRevisedRanksPPR(semMatrix, seeds, rel, irr, objList, usrMovies):
	N = len(objList)# Number of movies
	numSemantics = len(semMatrix[0])
	R = len(rel)
	Q = len(irr)
	ranks = {}
	r = np.zeros(numSemantics)
	q = np.zeros(numSemantics)
	n = np.zeros(numSemantics)
	p = np.zeros(numSemantics)
	u = np.zeros(numSemantics)
	#pre-calculating ri values
	for i in rel:
		#print("relevent =",semMatrix[i])
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				r[sem] += 1
	#pre-calculating qi values
	for i in irr:
		#print("irrelevant =", semMatrix[i])
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				q[sem] += 1
	#pre-calculating ni values
	for i in range(N):
		for sem in range(numSemantics):
			if(semMatrix[i][sem] != 0):
				n[sem] += 1
	#pre-calculating pi and ui values for the formula
	for i in range(len(r)):
		p[i] = (r[i]+n[i]/N)/(R+1)
		u[i] = (q[i]+n[i]/N)/(Q+1)
	pSum = np.sum(p)
	uSum = np.sum(u)
	if(pSum == 0): pSum = 1
	if(uSum == 0): uSum = 1
	p = p/pSum
	u = u/uSum
	print("\np =", p)
	print("\nu =", u)
	for sem in range(numSemantics):
		nr = p[sem] * (1-u[sem])
		dr = u[sem] * (1-p[sem])
		#print(nr,dr)
		if(nr != 0 and dr != 0 and nr != dr):
			sim = math.log(nr/dr)
		else:
			sim = 1
		for i in range(N):
			semMatrix[i][sem] = semMatrix[i][sem]*sim
	matrix = np.matmul(semMatrix,np.transpose(semMatrix))
	seedMat = ppr.formSeed(seeds, objList)
	pprOut = ppr.personalizedPageRank(matrix, seedMat, 0.15)
	rankedRes = ppr.rankedList(pprOut, objList, usrMovies, N)
	#print(rankedRes)
	return rankedRes
