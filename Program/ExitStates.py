# ExitStates.py
# Derek Schlabach
# Accept state for when Exit is called

from Singleton import *

@Singleton
class Exit(object):
	def isAccept(self):
		return True
	
	def prompt(self):
		return ""

	def getDict(self):
		return None

	def act(self, entry):
		print "Exiting... exited."
		exit(0)
