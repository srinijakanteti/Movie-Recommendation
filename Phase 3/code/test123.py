import math
import utils
semMatrix = [[1,0,3,2],
			 [0,1,0,5],
			 [7,0,2,0],
			 [6,5,2,0],
			 [4,1,0,0]]
rel = [1,2]
irrel = [0,3]
N = 5
R = 2
def getRevisedRanks(semMatrix, rel, irrel):
	movies = len(semMatrix)
	movieVectors = len(semMatrix[0])
	ranks = {}
	r = [0 for i in range(0,movieVectors)]
	n = [0 for i in range(0,movieVectors)]
	p = [0 for i in range(0,movieVectors)]
	u = [0 for i in range(0,movieVectors)]
	result = [[0 for i in range(movieVectors)] for j in range(0,movies)]
	#pre-calculating ri values	
	for movie in rel:
			for movieVector in range(0,movieVectors):
				if(semMatrix[movie][movieVector] != 0):
					r[movieVector] += 1
	#pre-calculating ni values		
	for movie in range(0,movies):
		for movieVector in range(0,movieVectors):
			if(semMatrix[movie][movieVector] != 0):
				n[movieVector] += 1
	print(n)
	#pre-calculating pi and ui values for the formula
	for movieVector in range(0,movieVectors):
		p[movieVector] = (r[movieVector] + n[movieVector]/N)/(R + 1)
		u[movieVector] = (n[movieVector] - r[movieVector] +n[movieVector]/N)/(N - R + 1)
	print(p)
	print(u)
	#computing the values of sim(mi) for each movie mi
	for movieVector in range(0,movieVectors):
		q = math.log((p[movieVector]*(1-u[movieVector]))/(u[movieVector]*(1-p[movieVector])))
		for movie in range(0,movies):
			result[movie][movieVector] = semMatrix[movie][movieVector] * q
	print("result = ",result)
	for movie in range(0,movies):
		ranks[movie] = sum(result[movie])
	return ranks
revisedRanks = getRevisedRanks(semMatrix, rel, irrel)
revisedRanks = utils.sortByValue(revisedRanks)
print(revisedRanks)