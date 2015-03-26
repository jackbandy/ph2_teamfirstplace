# Seth Wulbecker
# The line of singletons for save states
# Calls the load functions and then looks for the file to load

from Singleton import *
import Data
import PhaseStates
import Memento
import pickle

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
		Data.Data.loadFileName = entry


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
		file = open(Data.Data.loadFileName, 'rb')
		dataToLoad = pickle.load(file)
		file.close()
		Memento.Memento().loadMemento(dataToLoad)
		if (Data.Data.stokesOrNS == "stokes"):
			Data.Data.form = StokesVGPFormulation(Data.Data.spaceDim, Data.Data.useConformingTraces, Data.Data.mu)
			Data.Data.form.initializeSolution(Data.Data.loadFileName, Data.Data.polyOrder, Data.Data.delta_k)
		elif(Data.Data.stokesOrNS == "navier-stokes"):
			Data.Data.form = NavierStokesVGPFormulation(Data.Data.loadFileName, Data.Data.spaceDim, Data.Data.reynolds, Data.Data.polyOrder, Data.Data.delta_k)





