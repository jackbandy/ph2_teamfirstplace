# Seth Wulbecker
# The second and final class in the Load line of classes
# Accept state after name of file has been entered

from Singleton import *
import Data
import Phase2

@Singleton
class LoadFile(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return "Loading... loaded."

	def getDict(self):
		dict = {"": Phase2.Phase2.Instance()}
		return dict

	def act(self, entry):
		#Need BF to be restored
		loadedSolution = Data.Solution.load(form.bf(), meshAndSolutionPrefixString)
		#if reject, return null
		#if accept, return class to go to

