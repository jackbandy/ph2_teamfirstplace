# Seth Wulbecker
# The line of singletons for save states
# Calls the save functions and asks for name to save it as

from Singleton import *
import Data
import PhaseStates

@Singleton
class Save(object):

	def isAccept(self):
		return false
	
	def prompt(self):
		return "What would you like to call the solution and mesh files?"

	def getDict(self):
		dict = {"\w*": SaveFile.Instance()}
		return dict

	def act(self, entry):
		return null



@Singleton
class SaveFile(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return "Saving... saved."

	def getDict(self):
		dict = {"": PhaseStates.Phase2.Instance()}
		return dict

	def act(self, entry):
		Data.form.solution().save(entry)
