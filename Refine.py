# Seth Wulbecker
# The first class in the line of Refine classes
# Calls refine method and then searched for H or P refinement

from PyCamellia import *
from Singleton import *
import HorP

@Singleton
class Refine(object):

	def isAccept(self):
		return false
	
	def prompt(self):
		return "h or p refinement?"

	def getDict(self):
		dict = {"h": HorP.HorP.Instance(), "p": HorP.HorP.Instance()}
		return dict

	def act(self, entry):
		if (entry == "h")
			#set Data.refineType = h
		elif (entry == "p")
			#set Data.refineType = p
		return null
		#if reject, return null
		#if accept, return class to go to
