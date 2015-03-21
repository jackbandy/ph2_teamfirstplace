from Singleton import *
from PyCamellia import *
from Data import *

@Singleton

class Phase1(object):

	def prompt(self):
		return 'You can now: create or load'
	def getDict(self):
		return {'load' : Load.Instance(),
			'create' : Create.Instance()}

	def act(self, input):
		return null
	
		
	def isAccept(self):
		return False

@Singleton

class Create(object):

	def prompt(self):
		return """Before we solve, I need to ask you some setup questions.\n
			Would you like to solve Stokes or Navier-Stokes?"""
	def getDict(self):
		return {'stokes' : Stokes.Instance(),
			'navier-stokes' : NavierStokes.Instance()}

	#expected input "stokes" or "navier-stokes"
	def act(self, input):
		stokesOrNS = input
	
	def isAccept(self):
		return False

@Singleton

class Stokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		reynolds = float(input)
	
	def isAccept(self):
		return False;


@Singleton

class NavierStokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		reynolds = float(input)
	
	def isAccept(self):
		return False;


@Singleton

class Reynolds(object):

	def prompt(self):
		return "Transient or steady state?"
	def getDict(self):

		return {"transient": Transient.Intance(),
			"steady state": SteadyState.Instance()}

	def act(self, input):
		#input should be "transient" or "steady state"
		transientOrSS = input;

	
	def isAccept(self):
		return False;



@Singleton

class SteadyState(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d+.\d+( )*x( )*\d+.\d+": MeshDim.Instance()}

	#expects input like "1.0 x 4.0"
	def act(self, input):
		theStrings = input.split()
		xdim = float(theStrings[0])
		ydim = float(theStrings[2])
	
	def isAccept(self):
		return False;

@Singleton

class Transient(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d+.\d+( )*x( )*\d+.\d+": MeshDim.Instance()}

	# input of format "2.0 x 5.0"
	def act(self, input):
		theStrings = input.split()
		xdim = float(theStrings[0])
		ydim = float(theStrings[2])
	
	def isAccept(self):
		return False;


@Singleton

class MeshDim(object):

	def prompt(self):
		return "How many elements in the initial mesh? (E.g. \"3 x 5\")"
	def getDict(self):
		return {"\d+( )*x\d+": MeshElem.Instance()}

	#input of format "2 x 5"
	def act(self, input):
		theStrings = input.split()
		xelem = float(input[0])
		yelem = float(input[2])
	
	def isAccept(self):
		return False;


@Singleton

class MeshElem(object):

	def prompt(self):
		return "What polynomial order? (1 to 9)"
	def getDict(self):
		#because we don't want to accept 0
		return {"1": polyOrder.Instance(), "2": polyOrder.Instance(), 
			"3": polyOrder.Instance(), "4": polyOrder.Instance(), 
			"5": polyOrder.Instance(), "6": polyOrder.Instance(), 
			"7": polyOrder.Instance(), "8": polyOrder.Instance()
			"9": polyOrder.Instance()}

	def act(self, input):
		polyOrder = float(input)
	
	def isAccept(self):
		return False;


@Singleton
class polyOrder(object):

	def prompt(self):
		return "How many inflow conditions?"
	def getDict(self):
		#Should we accept 0?
		if 
		return {"/d+": inflowCond.Instance()}

	def act(self, input):
		inflowCond = float(input)
	
	def isAccept(self):
		return False;

@Singleton
class inflowCond(object):

	def prompt(self):
		return "For inflow condition" + Data.inflowsAskedFor + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):
		#Should we accept 0?
		return {"/d+": inflowCondx.Instance()}

	def act(self, input):
		inflowCond = float(input)
	
	def isAccept(self):
		return False;


@Singleton
class inflowCondX(object):
	
	def prompt(self):
		return "How many inflow conditions?"
	def getDict(self):
		#Should we accept 0?
		return {"/d+": inflowCondx.Instance()}

	def act(self, input):
		polyOrder = float(input)
	
	def isAccept(self):
		return False;






#{"": Phase2.Instance()} is dictionary for any accept state






