import utils
class Tag:

	def __init__(self,id,timeStamp):
		self.id = id
		self.timeStamp = timeStamp
		if (timeStamp):
			(date,time) = timeStamp.split(" ")
			self.timeWeight = utils.wieghtedTime(date,time)

	def getId(self):
		return self.id
	def getTimeStamp(self):
		return self.timeStamp
	def getTimeWeight(self):
		return self.timeWeight