# Seth Wulbecker
# The line of singletons for save states
# Calls the load functions and then looks for the file to load

from Singleton import *
import Data
import PhaseStates

@Singleton
class Load(object):

	def isAccept(self):
		return false
	
	def prompt(self):
		return "What is the name of the file you would like to load?"

	def getDict(self):
		dict = {"\w*": LoadFile.Instance()}
		return dict

	def act(self, entry):
		return null



@Singleton
class LoadFile(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return "Loading... loaded."

	def getDict(self):
		dict = {"": PhaseStates.Phase2.Instance()}
		return dict

	def act(self, entry):
		#Need BF to be restored
		loadedSolution = Data.Solution.load(form.bf(), meshAndSolutionPrefixString)
