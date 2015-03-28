from Singleton import *
from PyCamellia import *
from Data import *


@Singleton
class Create(object):
	def prompt(self):
		return """Before we solve, I need to ask you some setup questions.\n
			Would you like to solve Stokes or Navier-Stokes?"""
	def getDict(self):
		return {'( )*stokes( )*' : Stokes.Instance(),
			'( )*navier-stokes( )*' : NavierStokes.Instance()}
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
		return {"( )*\d( )*": Reynolds.Instance()}
	def act(self, input):
		reynolds = float(input)
	def isAccept(self):
		return False;

@Singleton
class NavierStokes(object):
	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"( )*\d( )*": Reynolds.Instance()}
	def act(self, input):
		reynolds = float(input)
	def isAccept(self):
		return False;

@Singleton
class Reynolds(object):
	def prompt(self):
		return "Transient or steady state?"
	def getDict(self):
		return {"( )*transient( )*": Transient.Intance(),
			"( )*steady( )*state( )*": SteadyState.Instance()}
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
		return {"( )*([0-9]*\.[0-9]+|[0-9]+)*( )*x( )*([0-9]*\.[0-9]+|[0-9]+)( )*": MeshDim.Instance()}




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
		return {"( )*([0-9]*\.[0-9]+|[0-9]+)*( )*x( )*([0-9]*\.[0-9]+|[0-9]+)( )*": MeshDim.Instance()}
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
		return {"( )*\d+( )*x( )*\d+( )*": MeshElem.Instance()}
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
		return {"1": PolyOrder.Instance(), "2": PolyOrder.Instance(), 
			"3": PolyOrder.Instance(), "4": PolyOrder.Instance(), 
			"5": PolyOrder.Instance(), "6": PolyOrder.Instance(), 
			"7": PolyOrder.Instance(), "8": PolyOrder.Instance()
			"9": PolyOrder.Instance()}
	def act(self, input):
		polyOrder = float(input)
	def isAccept(self):
		return False;

@Singleton
class PolyOrder(object):
	def prompt(self):
		return "How many inflow conditions?"
	def getDict(self):
		#Should we accept 0? Right now we are.
		# if it's zero, don't ask for inflow conditions.
		return {"( )*0( )*": InflowCondVy.Instance(),
			"( )*/d+( )*": InflowCond.Instance()}
	def act(self, input):
		inflowCond = float(input)
		inflowsAskedFor = 0
	def isAccept(self):
		return False;

@Singleton
class InflowCond(object):
	def prompt(self):
		return ("For inflow condition " + str(inflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")")
	def getDict(self):
		#add spatial filter stuff
		return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)([0-9]*\.[0-9]+|[0-9]+)": InflowCondSpace.Instance(),
			"x(>|<)([0-9]*\.[0-9]+|[0-9]+),y=([0-9]*\.[0-9]+|[0-9]+)": InflowCondSpace.Instance(),
			"y=([0-9]*\.[0-9]+|[0-9]+),x(>|<)([0-9]*\.[0-9]+|[0-9]+)": InflowCondSpace.Instance(),
			"y(>|<)([0-9]*\.[0-9]+|[0-9]+),x=([0-9]*\.[0-9]+|[0-9]+)": InflowCondSpace.Instance()}
	def act(self, input):
		input = input.lower()
		input = re.split('([0-9]*\.[0-9]+|[0-9]+)')
		if input[0] == 'x=':
			spatial1 = SpatialFilter.matchingX(float(input[1]))
			if input[3]: ',y>':
				spatial2 = SpatialFilter.greaterThanY(float(input[4])
			elif input[3]: ',y<':
				spatial2 = SpatialFilter.lessThanY(float(input[4]))
		elif input[0] == 'x>':
			spatial1 = SpatialFilter.greaterThanX(float(input[1]))
			#must be y=	
			spatial2 = SpatialFilter.matchingY(float(input[4]))
		elif input[0] == 'x<':
			spatial1 = SpatialFilter.lessThanX(float(input[1]))	
			spatial2 = SpatialFilter.matchingThanY(float(input[4]))
		elif input[0] == 'y=':
			spatial1 = SpatialFilter.matchingY(float(input[1]))
			if input[3]==',x>':
				spatial2 = SpatialFilter.greaterThanX(float(input[4]))
			elif input[3]==',x<':
				spatial2 = SpatialFilter.lessThanX(float(input[4]))
		elif input[0] == 'y>':
			spatial1 = SpatialFilter.greaterThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		elif input[0] == 'y<':
			spatial1 = SpatialFilter.lessThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		spatialFilter = spatial1 and spatial2
		inflowSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class InflowCondSpace(object):
	def prompt(self):
		return "For inflow condition " + str(inflowsAskedFor + 1) + ", what is the x component of the velocity?"
	def getDict(self):
		return {"[\d\.xy\*\+-/^ ]+": InflowCondVx.Instance()}
	def act(self, input):
		input = "".join(input.split())
		function = (Parser.Parser.Instance()).parse(input)
		inflowXVelocity.append(function)
	def isAccept(self):
		return False;

@Singleton
class InflowCondVx(object):
	def prompt(self):
		return "For inflow condition " + str(inflowsAskedFor + 1) + ", what is the y component of the velocity?"
	def getDict(self):
		#if there's no more to be asked for
		if inflowsAskedFor == inflowCond - 1:
			return {"[\d\.xy\*\+-/^ ]+": InflowCondVy.Instance()}
		else
			return {"[\d\.xy\*\+-/^ ]+": InflowCond.Instance()}
	def act(self, input):
		inflowsAskedFor = inflowsAskedFor + 1
		input = "".join(input.split())
		function = (Parser.Parser.Instance()).parse(input)
		inflowYVelocity.append(function)
	def isAccept(self):
		return False;

#This will be the state after all inflow conditions are entered
@Singleton
class InflowCondVy(object):
	def prompt(self):
		return "How many outflow conditions?"
	def getDict(self):
		return {"0": OutflowSpace.Instance(),
			"/d+": OutflowCond.Instance()}
	def act(self, input):
		outflowsAskedFor = 0
		outflowCond = float(input)
	def isAccept(self):
		return False;

@Singleton
class OutflowCond(object):
	def prompt(self):
		return "For outflow condition " + str(outflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):
		if outflowsAskedFor == outflowCond - 1:
			return {"x=([0-9]*\.[0-9]+|[0-9]+),y(>|<)([0-9]*\.[0-9]+|[0-9]+)": OutflowSpace.Instance(),
			"x(>|<)([0-9]*\.[0-9]+|[0-9]+),y=([0-9]*\.[0-9]+|[0-9]+)": OutflowSpace.Instance(),
			"y=([0-9]*\.[0-9]+|[0-9]+),x(>|<)([0-9]*\.[0-9]+|[0-9]+)": OutflowSpace.Instance(),
			"y(>|<)([0-9]*\.[0-9]+|[0-9]+),x=([0-9]*\.[0-9]+|[0-9]+)": OutflowSpace.Instance()}
		else
			return {"x=([0-9]*\.[0-9]+|[0-9]+),y(>|<)([0-9]*\.[0-9]+|[0-9]+)": OutflowCond.Instance(),
			"x(>|<)([0-9]*\.[0-9]+|[0-9]+),y=([0-9]*\.[0-9]+|[0-9]+)": OutflowCond.Instance(),
			"y=([0-9]*\.[0-9]+|[0-9]+),x(>|<)([0-9]*\.[0-9]+|[0-9]+)": OutflowCond.Instance(),
			"y(>|<)([0-9]*\.[0-9]+|[0-9]+),x=([0-9]*\.[0-9]+|[0-9]+)": OutflowCond.Instance()}nce()}
	def act(self, input):
		outflowsAskedfor = outflowsAskedfor + 1
		input = input.lower()
		input = re.split('([0-9]*\.[0-9]+|[0-9]+)')
		if input[0] == 'x=':
			spatial1 = SpatialFilter.matchingX(float(input[1]))
			if input[3]: ',y>':
				spatial2 = SpatialFilter.greaterThanY(float(input[4])
			elif input[3]: ',y<':
				spatial2 = SpatialFilter.lessThanY(float(input[4]))
		elif input[0] == 'x>':
			spatial1 = SpatialFilter.greaterThanX(float(input[1]))
			#must be y=	
			spatial2 = SpatialFilter.matchingY(float(input[4]))
		elif input[0] == 'x<':
			spatial1 = SpatialFilter.lessThanX(float(input[1]))	
			spatial2 = SpatialFilter.matchingThanY(float(input[4]))
		elif input[0] == 'y=':
			spatial1 = SpatialFilter.matchingY(float(input[1]))
			if input[3]==',x>':
				spatial2 = SpatialFilter.greaterThanX(float(input[4]))
			elif input[3]==',x<':
				spatial2 = SpatialFilter.lessThanX(float(input[4]))
		elif input[0] == 'y>':
			spatial1 = SpatialFilter.greaterThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		elif input[0] == 'y<':
			spatial1 = SpatialFilter.lessThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		spatialFilter = spatial1 and spatial2
		outflowSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class OutflowSpace(object):
	def prompt(self):
		return "How many wall conditions?"
	def getDict(self):
		return {"0": InflowCondSpace.Instance(),
			"/d+": WallCond.Instance()}
	def act(self, input):
		wallCond = int(input)
		wallsAskedFor = 0
	def isAccept(self):
		return False;

@Singleton
class WallCond(object):
	def prompt(self):
		return "For wall condition" + str(wallsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):
		if wallsAskedFor == wallCond - 1:
			return {"x=([0-9]*\.[0-9]+|[0-9]+),y(>|<)([0-9]*\.[0-9]+|[0-9]+)": CreateAccept.Instance(),
			"x(>|<)([0-9]*\.[0-9]+|[0-9]+),y=([0-9]*\.[0-9]+|[0-9]+)": CreateAccept.Instance(),
			"y=([0-9]*\.[0-9]+|[0-9]+),x(>|<)([0-9]*\.[0-9]+|[0-9]+)": CreateAccept.Instance(),
			"y(>|<)([0-9]*\.[0-9]+|[0-9]+),x=([0-9]*\.[0-9]+|[0-9]+)": CreateAccept.Instance()}
		else:
			return {"x=([0-9]*\.[0-9]+|[0-9]+),y(>|<)([0-9]*\.[0-9]+|[0-9]+)": WallCond.Instance(),
			"x(>|<)([0-9]*\.[0-9]+|[0-9]+),y=([0-9]*\.[0-9]+|[0-9]+)": WallCond.Instance(),
			"y=([0-9]*\.[0-9]+|[0-9]+),x(>|<)([0-9]*\.[0-9]+|[0-9]+)": WallCond.Instance(),
			"y(>|<)([0-9]*\.[0-9]+|[0-9]+),x=([0-9]*\.[0-9]+|[0-9]+)": WallCond.Instance()}
	def act(self, input):
		wallsAskedFor = wallsAskedFor + 1
		
		input = input.lower()
		input = re.split('([0-9]*\.[0-9]+|[0-9]+)')
		if input[0] == 'x=':
			spatial1 = SpatialFilter.matchingX(float(input[1]))
			if input[3]: ',y>':
				spatial2 = SpatialFilter.greaterThanY(float(input[4])
			elif input[3]: ',y<':
				spatial2 = SpatialFilter.lessThanY(float(input[4]))
		elif input[0] == 'x>':
			spatial1 = SpatialFilter.greaterThanX(float(input[1]))
			#must be y=	
			spatial2 = SpatialFilter.matchingY(float(input[4]))
		elif input[0] == 'x<':
			spatial1 = SpatialFilter.lessThanX(float(input[1]))	
			spatial2 = SpatialFilter.matchingThanY(float(input[4]))
		elif input[0] == 'y=':
			spatial1 = SpatialFilter.matchingY(float(input[1]))
			if input[3]==',x>':
				spatial2 = SpatialFilter.greaterThanX(float(input[4]))
			elif input[3]==',x<':
				spatial2 = SpatialFilter.lessThanX(float(input[4]))
		elif input[0] == 'y>':
			spatial1 = SpatialFilter.greaterThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		elif input[0] == 'y<':
			spatial1 = SpatialFilter.lessThanY(float(input[1]))
			spatial2 = SpatialFilter.matchingX(float(input[4]))
		spatialFilter = spatial1 and spatial2
		wallSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class CreateAccept(object):
	def prompt(self):
		return ""
	def getDict(self):
		return {"": Phase2.Phase2.Instance()}
	def act(self):
		


	def isAccept(self):
		return True









