from Tag import Tag
import utils

class Movie:
	def __init__(self,id,rank):
		self.id = id
		self.tags = []
		self.unqTagIds = []
		# This rank and rank weight variables are for use in task one
		self.rank = rank
		self.rWeight = 0
		if(rank != 0):
			self.rWeight = utils.weightedRank(rank)

	def addTag(self,tagId,timeStamp):
		tag = Tag(tagId, timeStamp)
		self.tags.append(tag)
		self.addToUnq(tagId)

	def getId(self):
		return self.id

	def getTags(self):
		return self.tags

	def getRWeight(self):
		return self.rWeight

	def addToUnq(self,tagId):
		for tag in self.unqTagIds:
			if(tagId == tag):
				return
		self.unqTagIds.append(tagId)

	def getUnqTags(self):
		return self.unqTagIds