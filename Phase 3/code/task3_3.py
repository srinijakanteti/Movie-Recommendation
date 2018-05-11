from collections import defaultdict
from operator import itemgetter
import svd
import dbInfo as di
import numpy as np
import itertools
import tfIdfCalc as idf
np.set_printoptions(threshold=np.nan)
import random
import csv
import relFeedback as rf
import movieRecomm as mr

def loadDataset(filename):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
    trainingSet=['' for i in range(len(dataset))] 
    for i in range(len(dataset)):
        trainingSet[i]=dataset[i][0] 
    return trainingSet


class lshIdx:

    def __init__(self,hFamliy,k,L):
        self.hFamliy = hFamliy
        self.k = k
        self.L = 0
        self.hTables = []
        self.resize(L)

    def resize(self,L):
        if L < self.L:
            self.hTables = self.hTables[:L]
        else:
            hash_funcs = [[self.hFamliy.create_hash_func() for h in range(self.k)] for l in range(self.L,L)]
            self.hTables.extend([(g,defaultdict(lambda:[])) for g in hash_funcs])

    def hash(self,g,p):
        return self.hFamliy.combine([h.hash(p) for h in g])

    def index(self,points):
        self.points = points
        for g,table in self.hTables:
            for ix,p in enumerate(self.points):
                table[self.hash(g,p)].append(ix)
            print("Number of Unique movies :",len(table))
        self.tot_touched = 0
        self.num_queries = 0

    def query(self,q,metric,max_results):
        candidates = set()
        for g,table in self.hTables:
            matches = table.get(self.hash(g,q),[])
            candidates.update(matches)
        self.tot_touched += len(candidates)
        self.num_queries += 1
        candidates = [(ix,metric(q,self.points[ix])) for ix in candidates]
        candidates.sort(key=itemgetter(1))
        return candidates[:max_results]

    def getAvgTouch(self):
        return self.tot_touched/self.num_queries



def dot(u,v):
    return sum(ux*vx for ux,vx in zip(u,v))

class L2HashFamily:

    def __init__(self,w,d):
        self.w = w
        self.d = d

    def create_hash_func(self):
        return L2Hash(self.rand_vec(),self.rand_offset(),self.w)

    def rand_vec(self):
        return [random.gauss(0,1) for i in range(self.d)]

    def rand_offset(self):
        return random.uniform(0,self.w)

    def combine(self,hashes):
        return str(hashes)

class L2Hash:

    def __init__(self,r,b,w):
        self.r = r
        self.b = b
        self.w = w

    def hash(self,vec):
        return int((dot(vec,self.r)+self.b)/self.w)

def L2_norm(u,v):
        return sum((ux-vx)**2 for ux,vx in zip(u,v))**0.5


class LSHTester:
   
    def __init__(self,points,queries,num_neighbours):
        self.points = points
        self.queries = queries
        self.num_neighbours = num_neighbours

    def run(self,name,metric,hFamliy,kVal,lVal,qMov):
        
        exact_hits = [[ix for ix,dist in self.linear(q,metric,self.num_neighbours+1)] for q in self.queries]

        print (name)
        print ('L\tk\tacc\ttouch')
        for k in kVal:        # concatenating more hash functions increases selectivity
            lsh = lshIdx(hFamliy,k,0)
            for L in lVal:    # using more hash tables increases recall
                lsh.resize(L)
                lsh.index(self.points)

                correct = 0
                for q,hits in zip(self.queries,exact_hits):
                    lsh_hits = [ix for ix,dist in lsh.query(q,metric,self.num_neighbours+1)]
                    if lsh_hits == hits:
                        correct += 1
                #print ("{0}\t{1}\t{2}\t{3}".format(L,k,float(correct)/100,float(lsh.getAvgTouch())/len(self.points)))

        for q in self.queries:
            lsh_hits = [(ix,dist) for ix,dist in lsh.query(q,metric,self.num_neighbours+1)]
        print("ser no.\tmovieIds\tmovieNames")
        i = 0
        retArr = []
        for l,d in lsh_hits:
            if(movies[l] != qMov):
                i += 1
                print(i,"\t",movies[l],"\t\t",movieNames[l])
                retArr.append(movies[l])
        return retArr

    def linear(self,q,metric,max_results):
        """ brute force search by linear scan """
        candidates = [(ix,metric(q,p)) for ix,p in enumerate(self.points)]
        return sorted(candidates,key=itemgetter(1))[:max_results]



if __name__ == "__main__":
	trainingSet = []
	movies = loadDataset('foo.csv')
	numsemantics = 500
	allMovies = di.getAllMovies()
	tagIds = di.getAllTags()
	allTagLen = len(tagIds)
	movNames = di.getAllMovieNames()
	movieNames = np.array(['' for i in range(len(movies))])
	for i in range(len(allMovies)):
		mov = allMovies[i]
		if(mov[0] in movies):
			idx = movies.index(mov[0])
			movieNames[idx] = movNames[i][0]
	mat = np.zeros((len(movies),allTagLen))
	idfMovArr = idf.idfMovieTag()
	for i in range(len(movies)):
		mat[i] = idf.tfIdfMovieTag(movies[i], idfMovArr)
	a = svd.svdUout(mat,numsemantics)
	d = 5
	xmax = 20
	points = np.array(a)
	l = int(input("Enter number of layers:"))
	k = int(input("Enter number of hashes per layer:"))
	r = int(input("Enter number of neighbours:"))
	q = input("Enter query movieid:")
	ks = []
	ls = []
	ks.append(k)
	ls.append(l)
	query=[]
	query.append(q) 
	tagIds = di.getAllTags()
	allTagLen = len(tagIds)
	movieNames = di.getAllMovieNames()
	test = np.zeros((len(query),numsemantics))
	j=0
	for i in range(len(movies)):
		if movies[i] in query:
			print("query = ", query)
			test[j] = a[i] 
	num_neighbours = r
	rad = 0.07
	tester = LSHTester(points,test,num_neighbours)
	args = {'name':'L2',
			'metric':L2_norm,
			'hFamliy':L2HashFamily(rad,d),
			'kVal':ks,
			'lVal':ls,
			'qMov':q}
	rankedRes = tester.run(**args)
	print("ranks = ",rankedRes)

	relMoviesIdx = input("Relavent Movies = ").split(',')
	irrMoviesIdx = input("Irrelavent Movies = ").split(',')
	relMoviesIdx, irrMoviesIdx, irrMovies = mr.getRelIrrMov(rankedRes, relMoviesIdx, irrMoviesIdx)
	R = np.zeros((len(relMoviesIdx),numsemantics))
	I = np.zeros((len(irrMoviesIdx),numsemantics))
	#print(a.shape, relMoviesIdx, irrMoviesIdx)
	for i in range(len(relMoviesIdx)):
		R[i] = a[relMoviesIdx[i]]
		#print("R = ", R[i])
	for i in range(len(irrMoviesIdx)):
		I[i] = a[irrMoviesIdx[i]]
	#print(test)
	test[0] = rf.relFeedback(test[0], R, I)
	tester = LSHTester(points,test,num_neighbours)
	tester.run(**args)
