# Seth Wulbecker
# The second class in the Refine line of classes
# class made after H or P is chosen for refine

from PyCamellia import *
from Singleton import *
import AutoOrMan
import Data

@Singleton
class HorP(object):
	p = re.compile("(%d,)*%d")

	def isAccept(self):
		return false
	
	def prompt(self):
		return "Which elements? You can specify active element numbers 0,1,2,5,8,9,10,... or auto."

	def getDict(self):
		dict = {"auto": AutoOrMan.AutoOrMan.Instance(), "(\d+,)*\d+": AutoOrMan.AutoOrMan.Instance()}
		return dict

	def act(self, entry):
		if (entry == "auto")
			Data.aorm = "auto"
		else
			manNums = entry.split(",")
			manNums = [int(i) for i in manNums]
			Data.aorm = "manual"
			Data.manualElems = manNums
		return null
		#if reject, return null
		#if accept, return class to go to
