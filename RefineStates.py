# Seth Wulbecker
# The first class in the line of Refine classes
# Calls refine method and then searched for H or P refinement

from PyCamellia import *
from Singleton import *
import Data
import PhaseStates

@Singleton
class Refine(object):

	def isAccept(self):
		return False
	
	def prompt(self):
		return "h or p refinement?"

	def getDict(self):
		dict = {"h": HorP.Instance(), "p": HorP.Instance()}
		return dict

	def act(self, entry):
		if (entry == "h"):
			Data.horp = "h"
		elif (entry == "p"):
			Data.horp = "p"



@Singleton
class HorP(object):

	def isAccept(self):
		return False
	
	def prompt(self):
		return "Which elements? You can specify active element numbers 0,1,2,5,8,9,10,... or auto."

	def getDict(self):
		dict = {"auto": AutoOrMan.Instance(), "(\d+,)*\d+": AutoOrMan.Instance()}
		return dict

	def act(self, entry):
		if (entry == "auto"):
			Data.aorm = "auto"
		else:
			manNums = entry.split(",")
			manNums = [int(i) for i in manNums]
			Data.aorm = "manual"
			Data.manualElems = manNums




@Singleton
class AutoOrMan(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return ""

	def getDict(self):
		dict = {"": PhaseStates.Phase2.Phase2.Instance()}
		return dict

	def act(self, entry):
		refinementNumber = 0
		if (Data.horp == "h"):
			if (Data.aorm == "auto"):
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.hRefine()
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
			elif (Data.aorm == "manual"):
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.hRefine(Data.manualElems)
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
		elif (Data.horp == "p"):
			if (Data.aorm == "auto"):
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.pRefine()
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
			elif (Data.aorm == "manual"):
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.pRefine(Data.manualElems)
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))



