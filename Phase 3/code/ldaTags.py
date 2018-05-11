import dbInfo as di
from gensim import corpora, models

def ldaInputTags(genre):
    movies = di.getGenreMovies(genre)
    movieTags = []
    for movie in movies:
        arr = []
        tags = di.getMovieTags(movie[0])
        for tag in tags:
            arr.append(tag[0])
        if(len(tags) != 0):
            movieTags.append(arr)
    return movieTags