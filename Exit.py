# Seth Wulbecker
# Accept state for when Exit is called

from Singleton import *

@Singleton
class Exit(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		print("Exiting... exited.")
		return ""

	def getDict(self):
		return null

	def act(self, entry):
		#if reject, return null
		#if accept, return class to go to
