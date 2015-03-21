# Seth Wulbecker
# The first class in the Load line of classes
# Calls the load functino and then looks for the file to load

from Singleton import *
import LoadFile

@Singleton
class Load(object):

	def isAccept(self):
		return false
	
	def prompt(self):
		return "What is the name of the file you would like to load?"

	def getDict(self):
		dict = {"\w*": LoadFile.LoadFile.Instance()}
		return dict

	def act(self, entry):
		return null
		#if reject, return null
		#if accept, return class to go to
