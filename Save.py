# Seth Wulbecker
# The first class in the Save line of classes
# Calls the save functino and asks for name to save it as

from Singleton import *
import SaveFile

@Singleton
class Save(object):

	def isAccept(self):
		return false
	
	def prompt(self):
		return "What would you like to call the solution and mesh files?"

	def getDict(self):
		dict = {"\w*": SaveFile.SaveFile.Instance()}
		return dict

	def act(self, entry):
		return null
		#if reject, return null
		#if accept, return class to go to
