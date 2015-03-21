# Seth Wulbecker
# The third and last class of the Refine line of classes
# Accept state after auto or manual has been chosen

from PyCamellia import *
from Singleton import *
import Phase2

@Singleton
class AutoOrMan(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return ""

	def getDict(self):
		dict = {"": Phase2.Phase2.Instance()}
		return dict

	def act(self, entry):
		refinementNumber = 0
		if (Data.horp = "h")
			if (Data.aorm = "auto")
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.hRefine()
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
			elif (Data.aorm = "manual")
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.hRefine(Data.manualElems)
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
		elif (Data.horp = "p")
			if (Data.aorm = "auto")
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.pRefine()
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
			elif (Data.aorm = "manual")
				while energyError > threshold and refinementNumber <= 8:
  					Data.form.pRefine(Data.manualElems)
  					Data.form.solve()
  					energyError = Data.form.solution().energyErrorTotal()
  					refinementNumber += 1
  					elementCount = Data.mesh.numActiveElements()
  					globalDofCount = Data.mesh.numGlobalDofs()
  					print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  					print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
		return null
		#if reject, return null
		#if accept, return class to go to
