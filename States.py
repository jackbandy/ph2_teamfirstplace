from Singleton import *
from PyCamellia import *

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

	def act(self, input):
		return null
	
	def isAccept(self):
		return False

@Singleton

class Stokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		return null
	
	def isAccept(self):
		return False;


@Singleton

class NavierStokes(object):

	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"\d": Reynolds.Instance()}

	def act(self, input):
		return null
	
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
		return null
	
	def isAccept(self):
		return False;



@Singleton

class SteadyState(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d(\d)*.\d(\d)*" MeshDim.Instance()}


	def act(self, input):
		return null
	
	def isAccept(self):
		return False;

@Singleton

class Transient(object):

	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):

		return {"\d(\d)*.\d(\d)*" MeshDim.Instance()}


	def act(self, input):
		return null
	
	def isAccept(self):
		return False;





