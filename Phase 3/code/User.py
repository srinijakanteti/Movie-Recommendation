class User:

	def __init__(self,id):
		self.id = id
		self.movies = []
		self.unqTags = []
		
	def addMovie(self,movie):
		self.movies.append(movie)

	def getId(self):
		return self.id
		
	def getMovies(self):
		return self.movies

	#Run this method after all the movies watched by the user is added to the object
	def setUnqTags(self):
		for movie in self.movies:
			for tag in movie.tags:
				tagId = tag.getId()
				if(tagId not in self.unqTags):
					self.unqTags.append(tagId)

	def getUnqTags(self):
		return self.unqTags