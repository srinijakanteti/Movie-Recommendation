import dbInfo as di
from gensim import corpora, models

def ldaInputActors(genre):
    movies = di.getGenreMovies(genre)
    movieActors = []
    for movie in movies:
        arr = []
        actors = di.getMovieActorIds(movie[0])
        for actor in actors:
            arr.append(actor[0])
        movieActors.append(arr)
    return movieActors
