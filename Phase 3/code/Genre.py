class Genre:

	def __init__(self,name):
		self.name = name
		self.movies = []
		self.unqTags = []

	def addMovie(self,movie):
		self.movies.append(movie)
		
	def getMovies(self):
		return self.movies

	#Run this method after all the movies of an genre is added to the object
	def setUnqTags(self):
		for movie in self.movies:
			for tag in movie.tags:
				tagId = tag.getId()
				if(tagId not in self.unqTags):
					self.unqTags.append(tagId)

	def getUnqTags(self):
		return self.unqTags