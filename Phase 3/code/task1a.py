import svd
import dbInfo as db
import numpy as np
import utils
import ldaTags as lda1
from gensim import corpora,models
np.set_printoptions(threshold=np.nan)

numSemantics = 4
genre = input("Enter Genre: ")
mat = svd.genSVDMatrix(genre)
if(len(mat)<numSemantics or len(mat[0])<numSemantics):
	print("cant report top semantics")
else:
	svdSem = svd.svdCalc(mat,numSemantics)
	pcaSem = svd.svdCalc(np.matmul(np.transpose(mat),mat),numSemantics)
	allTags = db.getAllTags()
	print("\n\nSVD Decomposed top semantics:")
	for sem in svdSem:
		print("\n\n",utils.rankSem(sem, allTags))
	print("\n\nPCA Decomposed top semantics:")
	for sem in pcaSem:
		print("\n\n",utils.rankSem(sem, allTags))
X = lda1.ldaInputTags(genre)
dictionary = corpora.Dictionary(X)
#print(dictionary)
#print(dictionary.token2id)
corpus = [dictionary.doc2bow(x) for x in X]
#print(corpus)
ldamodel = models.LdaModel(corpus, id2word = dictionary, num_topics = numSemantics)
ldaSems = ldamodel.print_topics(num_topics = -1, num_words = len(dictionary))
print("\n\nLDA Decomposed top semantics:")
for sem in ldaSems:
    print("\n\n",sem)
print("\nThe above ids are Tag IDs")
