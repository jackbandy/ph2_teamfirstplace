from Singleton import *
from PyCamellia import *
from Data import *
import re

data = Data()

#removes white space and makes lower case
def formatInput(string):
	inputString = inputString.lower()
	return inputString = "".join(inputString.split())

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
                input = formatInput(input)
		data.stokesOrNS = input
	def isAccept(self):
		return False

@Singleton
class Stokes(object):
	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"( )*\d( )*": Reynolds.Instance()}
	def act(self, input):
		input = formatInput(input)
		data.reynolds = float(input)
	def isAccept(self):
		return False;

@Singleton
class NavierStokes(object):
	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"( )*\d( )*": Reynolds.Instance()}
	def act(self, input):
		input = formatInput(input)
		data.reynolds = float(input)
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
		input = formatInput(input)
		#input should be "transient" or "steadystate"
		data.transientOrSS = input;
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
		input = formatInput(input)
		data.xdim = float(input[0])
		data.ydim = float(input[2])
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
		input = formatInput(input)
		data.xdim = float(input[0])
		data.ydim = float(input[2])
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
		input = formatInput(input)
		data.xelem = float(input[0])
		data.yelem = float(input[2])
	def isAccept(self):
		return False;

@Singleton
class MeshElem(object):
	def prompt(self):
		return "What polynomial order? (1 to 9)"
	def getDict(self):
		#because we don't want to accept 0
		return {"( )*1( )*": PolyOrder.Instance(), "( )*2( )*": PolyOrder.Instance(), 
			"( )*3( )*": PolyOrder.Instance(), "( )*4( )*": PolyOrder.Instance(), 
			"( )*5( )*": PolyOrder.Instance(), "( )*6( )*": PolyOrder.Instance(), 
			"( )*7( )*": PolyOrder.Instance(), "( )*8( )*": PolyOrder.Instance()
			"( )*9( )*": PolyOrder.Instance()}
	def act(self, input):
		input = formatInput(input)
		data.polyOrder = float(input)
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
		input = formatInput(input)
		data.inflowCond = float(input)
		data.inflowsAskedFor = 0
	def isAccept(self):
		return False;

@Singleton
class InflowCond(object):
	def prompt(self):
		return ("For inflow condition " + str(inflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")")
	def getDict(self):
		#add spatial filter stuff
		return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": InflowCondSpace.Instance(),
			"( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": InflowCondSpace.Instance(),
			"( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": InflowCondSpace.Instance(),
			"( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": InflowCondSpace.Instance()}
	def act(self, input):
		input = formatInput(input)
		input = re.split('( )*([0-9]*\.[0-9]+|[0-9]+)( )*')
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
		data.inflowSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class InflowCondSpace(object):
	def prompt(self):
		return "For inflow condition " + str(data.inflowsAskedFor + 1) + ", what is the x component of the velocity?"
	def getDict(self):
		return {"[\d\.xy\*\+-/^ ]+": InflowCondVx.Instance()}
	def act(self, input):
		input = formatInput(input)
		function = (Parser.Parser.Instance()).parse(input)
		data.inflowXVelocity.append(function)
	def isAccept(self):
		return False;

@Singleton
class InflowCondVx(object):
	def prompt(self):
		return "For inflow condition " + str(data.inflowsAskedFor + 1) + ", what is the y component of the velocity?"
	def getDict(self):
		#if there's no more to be asked for
		if inflowsAskedFor == inflowCond - 1:
			return {"[\d\.xy\*\+-/^ ]+": InflowCondVy.Instance()}
		else
			return {"[\d\.xy\*\+-/^ ]+": InflowCond.Instance()}
	def act(self, input):
		data.inflowsAskedFor = data.inflowsAskedFor + 1
		input = formatInput(input)
		function = (Parser.Parser.Instance()).parse(input)
		data.inflowYVelocity.append(function)
	def isAccept(self):
		return False;

#This will be the state after all inflow conditions are entered
@Singleton
class InflowCondVy(object):
	def prompt(self):
		return "How many outflow conditions?"
	def getDict(self):
		return {"( )*0( )*": OutflowSpace.Instance(),
			"( )*/d+( )*": OutflowCond.Instance()}
	def act(self, input):
		input = formatInput(input)
		data.outflowsAskedFor = 0
		data.outflowCond = float(input)
	def isAccept(self):
		return False;

@Singleton
class OutflowCond(object):
	def prompt(self):
		return "For outflow condition " + str(data.outflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):

		if data.outflowsAskedFor == data.outflowCond - 1:
			return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowSpace.Instance(),
				"( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowSpace.Instance(),
				"( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowSpace.Instance(),
				"( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowSpace.Instance()}
		else:
			return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowCond.Instance(),
				"( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowCond.Instance(),
				"( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowCond.Instance(),
				"( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowCond.Instance()}

	def act(self, input):
		data.outflowsAskedfor = data.outflowsAskedfor + 1
		input = formatInput(input)
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
		data.outflowSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class OutflowSpace(object):
	def prompt(self):
		return "How many wall conditions?"
	def getDict(self):
		return {"( )*0( )*": InflowCondSpace.Instance(),
			"( )*/d+( )*": WallCond.Instance()}
	def act(self, input):
		input = formatInput(input)
		data.wallCond = int(input)
		data.wallsAskedFor = 0
	def isAccept(self):
		return False;

@Singleton
class WallCond(object):
	def prompt(self):
		return "For wall condition" + str(data.wallsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):
		if data.wallsAskedFor == data.wallCond - 1:
			return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": CreateAccept.Instance(),
				"( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": CreateAccept.Instance(),
				"( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": CreateAccept.Instance(),
				"( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": CreateAccept.Instance()}
		else:
			return {"( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": WallCond.Instance(),
				"( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": WallCond.Instance(),
				"( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": WallCond.Instance(),
				"( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": WallCond.Instance()}
	def act(self, input):
		data.wallsAskedFor = data.wallsAskedFor + 1
		
		input = formatInput(input)
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
		data.wallSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class CreateAccept(object):
	def prompt(self):
		return ""
	def getDict(self):
		return {"": Phase2.Phase2.Instance()}
	def act(self):
		if data.stokesOrNS == 'stokes':
			solveStokes()
		elif data.stokesOrNS == 'navier-stokes':
			solveNavier()

	def isAccept(self):
		return True



def solveNavier():
	spaceDim = 2
	Re = data.reynolds
	dims = [data.xdim,data.ydim]
	numElements = [data.xelem,data.yelem]
	x0 = [0.,0.]
	meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
	#polyOrder
	delta_k = 1

	form = NavierStokesVGPFormulation(meshTopo,Re,data.polyOrder,delta_k)

	form.addZeroMeanPressureCondition()

	#assume 1 inflow and outflow condition. Ideally this wouldn't be

	inflowVelocity = Function.vectorize(data.inflowXVelocity[0], data.inflowYVelocity[0])
	form.addInflowCondition(data.inflowSpatialFilters[0],data.inflowVelocity)
	form.addOutflowCondition(data.outflowSpatialFilters[0])
	wallBuilding = data.inflowSpatialFilters[0] or data.outflowSpatialFilters[0]

	for i in range(1, data.inflowCond):
		wallBuilding = wallBuilding or data.inflowSpatialFilters[i]
		inflowVelocity = Function.vectorize(data.inflowXVelocity[i], data.inflowYVelocity[i])
		form.addInflowCondition(data.inflowSpatialFilters[i], inflowVelocity)

	for i in range(1, data.outflowcond):
		form.addOutflowCondition(data.outflowSpatialFilters[i])
		wallBuilding = wallBuilding or data.outflowSpatialFilters[i]

	wall = SpatialFilter.negatedFilter(wallBuilding)
	form.addWallCondition(wall)

	refinementNumber = 0
	nonlinearThreshold = 1e-3

	#nonlinear Solve
	maxSteps = 10
	normOfIncrement = 1
	stepNumber = 0
	while stepNumber < maxSteps:
		form.solveAndAccumulate()
		normOfIncrement = form.L2NormSolutionIncrement()
		print("L^2 norm of increment: %0.3f" % normOfIncrement)
		stepNumber += 1



	mesh = form.solution().mesh();


def solveStokes():


	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
	dims = [data.xdim,data.ydim]
	numElements = [data.xelem,data.yelem]
	x0 = [0.,0.]
	#polyorder
	meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
	delta_k = 1

	form.initializeSolution(meshTopo,data.polyOrder,delta_k)
	form.addZeroMeanPressureCondition()

	inflowVelocity = Function.vectorize(data.inflowXVelocity[0], data.inflowYVelocity[0])
	form.addInflowCondition(data.inflowSpatialFilters[0],data.inflowVelocity)
	form.addOutflowCondition(data.outflowSpatialFilters[0])
	wallBuilding = data.inflowSpatialFilters[0] or data.outflowSpatialFilters[0]

	for i in range(1, data.inflowCond):
		wallBuilding = wallBuilding or data.inflowSpatialFilters[i]
		inflowVelocity = Function.vectorize(data.inflowXVelocity[i], data.inflowYVelocity[i])
		form.addInflowCondition(data.inflowSpatialFilters[i], inflowVelocity)

	for i in range(1, data.outflowcond):
		form.addOutflowCondition(data.outflowSpatialFilters[i])
		wallBuilding = wallBuilding or data.outflowSpatialFilters[i]

	wall = SpatialFilter.negatedFilter(wallBuilding)
	form.addWallCondition(wall)


	refinementNumber = 0
	form.solve()
	mesh = form.solution().mesh();
	energyError = form.solution().energyErrorTotal()
	elementCount = mesh.numActiveElements()
	globalDofCount = mesh.numGlobalDofs()
	print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
	print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
	threshold = .05


	while refinementNumber <= 10:
		form.hRefine()
		form.solve()
		energyError = form.solution().energyErrorTotal()
		refinementNumber += 1
		elementCount = mesh.numActiveElements()
		globalDofCount = mesh.numGlobalDofs()
		print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
		print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))


	perCellError = form.solution().energyErrorPerCell()
















