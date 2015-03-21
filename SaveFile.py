# Seth Wulbecker
# The second and final class in the Save line of classes
# Accept state after name of file has been entered

from Singleton import *
import Data
import Phase2

@Singleton
class SaveFile(object):

	def isAccept(self):
		return true
	
	def prompt(self):
		return "Saving... saved."

	def getDict(self):
		dict = {"": Phase2.Phase2.Instance()}
		return dict

	def act(self, entry):
		Data.form.solution().save(entry)
		#if reject, return null
		#if accept, return class to go to
