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
		Data.stokesOrNS = input
	
	def isAccept(self):
		return False

@Singleton

class Stokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		Data.reynolds = input
	
	def isAccept(self):
		return False;


@Singleton

class NavierStokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		Data.reynolds = input
	
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
		Data.transientOrSS = input;

	
	def isAccept(self):
		return False;



@Singleton

class SteadyState(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d+.\d+( )*x( )*\d+.\d+": MeshDim.Instance()}


	def act(self, input):
		return null
	
	def isAccept(self):
		return False;

@Singleton

class Transient(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d+.\d+( )*x( )*\d+.\d+": MeshDim.Instance()}

	# expects string input 
	def act(self, input):
		#FIX THIS. expects input like "1.0 x 4.0". need to take that apart.
		Data.xdim = float(input)
	
	def isAccept(self):
		return False;


@Singleton

class MeshDim(object):


	def prompt(self):
		return "How many elements in the initial mesh? (E.g. \"3 x 5\")"
	def getDict(self):

		return {"\d(\d)* x \d(\d)*": MeshElem.Instance()}


	def act(self, input):
		return null
	
	def isAccept(self):
		return False;










