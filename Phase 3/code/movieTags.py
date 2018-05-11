import dbInfo as di
import numpy as np
import lda
np.set_printoptions(threshold=np.nan)

movies = di.getAllMovies()
movies1 = tuple(movies)
tags = di.getAllTags()
tags1 = tuple(tags)
n1 = len(movies1)
n2 = len(tags)

movTag = []
for movie in movies1:
    arr = []
    for i in range(0,n2):
        arr.append(0)
    tgs = tuple(di.getMovieTags(movie[0]))
    for tag in tags1:
        for tg in tgs:
            if tag[0] == tg[0]:
                arr[tags1.index(tag)] += 1
                print("i = ",tags1.index(tag))
    movTag.append(arr)
movTag = np.array(movTag)
print(movTag)
#model = lda.LDA(n_topics = 500, n_iter = 100, random_state = 1)
#model.fit(movTag)
#doc2topic = model.doc_topic_

