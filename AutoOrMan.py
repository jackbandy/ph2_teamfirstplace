# Seth Wulbecker
# The third and last class of the Refine line of classes
# Accept state after auto or manual has been chosen

from PyCamellia import *
from Singleton import *
import #Phase2

@Singleton
class AutoOrMan(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return ""

	def getDict(self):
		dict = {"": #Phase2.Phase2.Instance()}
		return dict

	def act(self, entry):
		return null
		#if reject, return null
		#if accept, return class to go to
