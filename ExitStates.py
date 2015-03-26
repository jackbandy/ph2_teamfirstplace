# Seth Wulbecker
# Accept state for when Exit is called

from Singleton import *

@Singleton
class Exit(object):
	def isAccept(self):
		return True
	
	def prompt(self):
		return "Exiting... exited."

	def getDict(self):
		return null

	def act(self, entry):
		exit(0)
