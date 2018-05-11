import svd
import dbInfo as db
import numpy as np
import ldaActors as lda1
from gensim import corpora,models
import tfCalc as tf

numSemantics = 4
genre = input("Enter Genre: ")
'''
def genSVDMatrix2(genrelist):
	genObj = tf.createGenObj(genrelist)
	movies = genObj.getMovies()
	actorlist = db.getAllActors()
	movielist = db.getActorMovies()
	actor_rank = db.getActorRanks()
	Matrix = [[0 for x in range(len(actorlist))]for y in range(0,len(movies))]
	x=0;
	for movie in movies:
		for actor in actorlist:
			movielist = db.getActorMovies(actor)
			if movie == movielist(actor):
				rank = db.getActorRanks(actor[0])
				actorspace[movie][actor] = rank[actor]
			x=x+1
	return actorspace

def Calcsvd(A):
	U, s, V = np.linalg.svd(A,0)
	return U,s,V


def Calcpca(A):
	M = np.zeros((len(A),len(A[0])))
	A_Tr = np.transpose(A)
	Input_PCA = np.zeros((3, 3))

	for i in range(len(A)):
	# iterate through columns of Y
		for j in range(len(A_Tr[0])):
	# iterate through rows of Y
			for k in range(len(A_Tr)):
				M[i][j] += A[i][k] * A_Tr[k][j]
	u,s,v = svd.Calcsvd(M)
	allTagLen = len(db.getAllTags())
	a=np.zeros((4,allTagLen))
	for i in range(4):
		for j in range(allTagLen):
			a[i][j] = v[i][j]

	return a


genre = input("Enter Genre: ")
Mat = genSVDMatrix2(genre)
if(len(Mat)<4 or len(Mat[0])<4):
	print("cant report top 4 semantics")
else:
	u,s,v = Calcsvd(Mat)
	allTags = db.getAllTags()
	allTagLen = len(allTags)
	a=np.zeros((4,allTagLen))
	for i in range(4):
		for j in range(allTagLen):
			a[i][j] = v[i][j]
	print("Tags order = ",allTags)
	print("SVD decomposed top 4 semantics",a)
	print("PCA Decomposition: ",Calcpca(Mat))

'''

X = lda1.ldaInputActors(genre)
#print(X)

dictionary = corpora.Dictionary(X)
#print(dictionary)
#print(dictionary.token2id)
corpus = [dictionary.doc2bow(x) for x in X]
#print(corpus)
ldamodel = models.LdaModel(corpus, id2word = dictionary, num_topics = numSemantics)
semantics = ldamodel.print_topics(num_topics = -1, num_words = len(dictionary))

print("\nLDA Decomposed top semantics:")
for i,sem in semantics:
    print("\n",sem)

print("\nThe above ids are Actor IDs")