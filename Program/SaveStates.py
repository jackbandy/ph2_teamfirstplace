# Seth Wulbecker
# The line of singletons for save states
# Calls the save functions and asks for name to save it as

from Singleton import *
import Data
import PhaseStates
import pickle
import Memento

@Singleton
class Save(object):

	def isAccept(self):
		return False
	
	def prompt(self):
		return "What would you like to call the solution and mesh files?"

	def getDict(self):
		dict = {"0\w*": SaveFile.Instance()}
		return dict

	def act(self, entry):
		Data.Data.saveFileName = entry
		print ("Saving to " + entry)


@Singleton
class SaveFile(object):

	def isAccept(self):
		return True
	
	def prompt(self):
		return ""

	def getDict(self):
		dict = {"": PhaseStates.Phase2.Instance()}
		return dict

	def act(self, entry):
		Data.Data.form.solution().save(Data.Data.saveFileName)
		savedData = Memento.Memento().setMemento()
		file = open(Data.Data.saveFileName, 'wb')
		pickle.dump(savedData, file)
		file.close()
		print("...saved.")
		
