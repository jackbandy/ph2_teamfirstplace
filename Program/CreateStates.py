#Scott Wurtz

from Singleton import *
from PyCamellia import *
from Data import *
import re
import Parser
import PhaseStates

#removes white space and makes lower case
def formatInput(string):
	inputString = string.lower()
	return "".join(string.split())

@Singleton
class Create(object):
	def prompt(self):
		return "Before we solve, I need to ask you some setup questions. \nWould you like to solve Stokes or Navier-Stokes?"
	def getDict(self):
		return {'0( )*stokes( )*' : Reynolds.Instance(),
			'1( )*navier-stokes( )*' : NavierStokes.Instance()}
	#expected input "stokes" or "navier-stokes"
	def act(self, input):
                input = formatInput(input)
		Data.stokesOrNS = input
	def isAccept(self):
		return False
@Singleton
class NavierStokes(object):
	def prompt(self):
		return "What Reynolds number?"
	def getDict(self):
		return {"0( )*\d+( )*": Reynolds.Instance()}
	def act(self, input):
		input = formatInput(input)
		Data.reynolds = float(input)
	def isAccept(self):
		return False;

@Singleton
class Reynolds(object):
	def prompt(self):
		return "Transient or steady state?"
	def getDict(self):
		return {"0( )*transient( )*": Transient.Instance(),
			"1( )*steady( )*state( )*": SteadyState.Instance()}
	def act(self, input):
		input = formatInput(input)
		#input should be "transient" or "steadystate"
		Data.transientOrSS = input;
	def isAccept(self):
		return False;

@Singleton
class SteadyState(object):
	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):
		return {"0( )*([0-9]*\.[0-9]+|[0-9]+)*( )*x( )*([0-9]*\.[0-9]+|[0-9]+)( )*": MeshDim.Instance()}
	#expects input like "1.0 x 4.0"
	def act(self, input):
		input = formatInput(input)
		Data.xdim = float(input[0])
		Data.ydim = float(input[2])
	def isAccept(self):
		return False;

@Singleton
class Transient(object):
	def prompt(self):
		return "This solver handles rectangular meshes with lower-left corner at the origin. \n What are the dimensions of your mesh? (E.g., \"1.0 x 2.0\")"
	def getDict(self):
		return {"0( )*([0-9]*\.[0-9]+|[0-9]+)*( )*x( )*([0-9]*\.[0-9]+|[0-9]+)( )*": MeshDim.Instance()}
	# input of format "2.0 x 5.0"
	def act(self, input):
		input = formatInput(input)
		Data.xdim = float(input[0])
		Data.ydim = float(input[2])
	def isAccept(self):
		return False;

@Singleton
class MeshDim(object):
	def prompt(self):
		return "How many elements in the initial mesh? (E.g. \"3 x 5\")"
	def getDict(self):
		return {"0( )*\d+( )*x( )*\d+( )*": MeshElem.Instance()}
	#input of format "2 x 5"
	def act(self, input):
		input = formatInput(input)
		Data.xelem = int(input[0])
		Data.yelem = int(input[2])
	def isAccept(self):
		return False;

@Singleton
class MeshElem(object):
	def prompt(self):
		return "What polynomial order? (1 to 9)"
	def getDict(self):
		#because we don't want to accept 0
		return {"0( )*[1-9]( )*": PolyOrder.Instance()}
	def act(self, input):
		input = formatInput(input)
		Data.polyOrder = int(input)
	def isAccept(self):
		return False;

@Singleton
class PolyOrder(object):
	def prompt(self):
		return "How many inflow conditions (1 or more)?"
	def getDict(self):
		return {"0( )*[1-9]\d*( )*": InflowCond.Instance()}
	def act(self, input):
		input = formatInput(input)
		Data.inflowCond = int(input)
		Data.inflowsAskedFor = 0
	def isAccept(self):
		return False;

@Singleton
class InflowCond(object):
	def prompt(self):
		return ("For inflow condition " + str(Data.inflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")")
	def getDict(self):
		#add spatial filter stuff
		return {"0( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": InflowCondSpace.Instance(),
			"1( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": InflowCondSpace.Instance(),
			"2( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": InflowCondSpace.Instance(),
			"3( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": InflowCondSpace.Instance()}
	def act(self, input):
		input = formatInput(input)
		inputData = re.split('=|<|>|,', input)
		input = re.split('( )*([0-9]*\.[0-9]+|[0-9]+)( )*', input)
		
		if input[0] == 'x=':
			spatial1 = SpatialFilter.matchingX(float(inputData[1]))
			if input[4] == ',y>':
				spatial2 = SpatialFilter.greaterThanY(float(inputData[3]))
			elif input[4]== ',y<':
				spatial2 = SpatialFilter.lessThanY(float(inputData[3]))
		elif input[0] == 'x>':
			spatial1 = SpatialFilter.greaterThanX(float(inputData[1]))
			#must be y=	
			spatial2 = SpatialFilter.matchingY(float(inputData[3]))
		elif input[0] == 'x<':
			spatial1 = SpatialFilter.lessThanX(float(inputData[1]))	
			spatial2 = SpatialFilter.matchingY(float(inputData[3]))
		elif input[0] == 'y=':
			spatial1 = SpatialFilter.matchingY(float(inputData[1]))
			if input[4]==',x>':
				spatial2 = SpatialFilter.greaterThanX(float(inputData[3]))
			elif input[4]==',x<':
				spatial2 = SpatialFilter.lessThanX(float(inputData[3]))
		elif input[0] == 'y>':
			spatial1 = SpatialFilter.greaterThanY(float(inputData[1]))
			spatial2 = SpatialFilter.matchingX(float(inputData[3]))
		elif input[0] == 'y<':
			spatial1 = SpatialFilter.lessThanY(float(inputData[1]))
			spatial2 = SpatialFilter.matchingX(float(inputData[3]))
		spatialFilter = spatial1 & spatial2
		Data.inflowSpatialFilters.append(spatialFilter)
	def isAccept(self):
		return False;

@Singleton
class InflowCondSpace(object):
	def prompt(self):
		return "For inflow condition " + str(Data.inflowsAskedFor + 1) + ", what is the x component of the velocity?"
	def getDict(self):
		return {"0[\d\.xy\*\+-/^\(\) ]+": InflowCondVx.Instance()}
	def act(self, input):
		input = formatInput(input)
		function = (Parser.Parser.Instance()).parse(input)
		Data.inflowXVelocity.append(function)
	def isAccept(self):
		return False;

@Singleton
class InflowCondVx(object):
	def prompt(self):
		return "For inflow condition " + str(Data.inflowsAskedFor + 1) + ", what is the y component of the velocity?"
	def getDict(self):
		#if there's no more to be asked for
		if Data.inflowsAskedFor == Data.inflowCond - 1:
			return {"0[\d\.xy\*\+-/^\(\) ]+": InflowCondVy.Instance()}
		else:
			return {"0[\d\.xy\*\+-/^\(\) ]+": InflowCond.Instance()}
	def act(self, input):
		Data.inflowsAskedFor = Data.inflowsAskedFor + 1
		input = formatInput(input)
		function = (Parser.Parser.Instance()).parse(input)
		Data.inflowYVelocity.append(function)
	def isAccept(self):
		return False;

#This will be the state after all inflow conditions are entered
@Singleton
class InflowCondVy(object):
	def prompt(self):
		return "How many outflow conditions (1 or more)?"
	def getDict(self):
		return {"0( )*[1-9]\d*( )*": OutflowCond.Instance()}



	def act(self, input):
		input = formatInput(input)
		Data.outflowsAskedFor = 0
		Data.outflowCond = int(input)
	def isAccept(self):
		return False;

@Singleton
class OutflowCond(object):
	def prompt(self):
		return "For outflow condition " + str(Data.outflowsAskedFor + 1) + ", what region of space? (E.g. \"x=0.5, y > 3\")"
	def getDict(self):

		if Data.outflowsAskedFor == Data.outflowCond - 1:
			return {"0( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": CreateAccept.Instance(),
				"1( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": CreateAccept.Instance(),
				"2( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": CreateAccept.Instance(),
				"3( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": CreateAccept.Instance()}
		else:
			return {"0( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowCond.Instance(),
				"1( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowCond.Instance(),
				"2( )*y( )*=( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*": OutflowCond.Instance(),
				"3( )*y( )*(>|<)( )*([0-9]*\.[0-9]+|[0-9]+)( )*,( )*x( )*=( )*([0-9]*\.[0-9]+|[0-9]+( )*)": OutflowCond.Instance()}

	def act(self, input):
		Data.outflowsAskedFor = Data.outflowsAskedFor + 1
		input = formatInput(input)
		inputData = re.split('=|<|>|,', input)
		input = re.split('( )*([0-9]*\.[0-9]+|[0-9]+)( )*', input)
		
		if input[0] == 'x=':
			spatial1 = SpatialFilter.matchingX(float(inputData[1]))
			if input[4] == ',y>':
				spatial2 = SpatialFilter.greaterThanY(float(inputData[3]))
			elif input[4]== ',y<':
				spatial2 = SpatialFilter.lessThanY(float(inputData[3]))
		elif input[0] == 'x>':
			spatial1 = SpatialFilter.greaterThanX(float(inputData[1]))
			#must be y=	
			spatial2 = SpatialFilter.matchingY(float(inputData[3]))
		elif input[0] == 'x<':
			spatial1 = SpatialFilter.lessThanX(float(inputData[1]))	
			spatial2 = SpatialFilter.matchingY(float(inputData[3]))
		elif input[0] == 'y=':
			spatial1 = SpatialFilter.matchingY(float(inputData[1]))
			if input[4]==',x>':
				spatial2 = SpatialFilter.greaterThanX(float(inputData[3]))
			elif input[4]==',x<':
				spatial2 = SpatialFilter.lessThanX(float(inputData[3]))
		elif input[0] == 'y>':
			spatial1 = SpatialFilter.greaterThanY(float(inputData[1]))
			spatial2 = SpatialFilter.matchingX(float(inputData[3]))
		elif input[0] == 'y<':
			spatial1 = SpatialFilter.lessThanY(float(inputData[1]))
			spatial2 = SpatialFilter.matchingX(float(inputData[3]))
		spatialFilter = spatial1 & spatial2
		Data.outflowSpatialFilters.append(spatialFilter)

	def isAccept(self):
		return False;


@Singleton
class CreateAccept(object):
	def prompt(self):
		return ""
	def getDict(self):
		return {"": PhaseStates.Phase2.Instance()}
	def act(self, input):
		if Data.stokesOrNS == 'stokes' and Data.transientOrSS=='steadystate':
			Data.form = solveStokes()
		elif Data.stokesOrNS == 'stokes' and Data.transientOrSS=='transient':
			Data.form = solveStokesTransient()
		elif Data.stokesOrNS == 'navier-stokes':
			Data.form = solveNavier()

	def isAccept(self):
		return True



def solveNavier():
	spaceDim = 2
	Re = Data.reynolds
	dims = [Data.xdim,Data.ydim]
	numElements = [int(Data.xelem),int(Data.yelem)]
	x0 = [0.,0.]
	meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
	#polyOrder
	delta_k = 1

	form = NavierStokesVGPFormulation(meshTopo,Re,Data.polyOrder,delta_k)

	form.addZeroMeanPressureCondition()

	#assume 1 inflow and outflow condition. Ideally this wouldn't be

	inflowVelocity = Function.vectorize(Data.inflowXVelocity[0], Data.inflowYVelocity[0])
	form.addInflowCondition(Data.inflowSpatialFilters[0],inflowVelocity)
	form.addOutflowCondition(Data.outflowSpatialFilters[0])
	wallBuilding = Data.inflowSpatialFilters[0] | Data.outflowSpatialFilters[0]

	for i in range(1, Data.inflowCond):
		wallBuilding = wallBuilding | Data.inflowSpatialFilters[i]
		inflowVelocity = Function.vectorize(Data.inflowXVelocity[i], Data.inflowYVelocity[i])
		form.addInflowCondition(Data.inflowSpatialFilters[i], inflowVelocity)

	for i in range(1, Data.outflowCond):
		form.addOutflowCondition(Data.outflowSpatialFilters[i])
		wallBuilding = wallBuilding | Data.outflowSpatialFilters[i]

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
	return form

def solveStokes():


	spaceDim = 2
	useConformingTraces = False
	mu = 1.0
	form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
	dims = [Data.xdim,Data.ydim]
	numElements = [int(Data.xelem),int(Data.yelem)]
	x0 = [0.,0.]
	print "About to create mesh with dims " + str(dims) + " and elements " + str(numElements)
	#polyorder
	meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
	delta_k = 1

	form.initializeSolution(meshTopo,Data.polyOrder,delta_k)
	form.addZeroMeanPressureCondition()

	inflowVelocity = Function.vectorize(Data.inflowXVelocity[0], Data.inflowYVelocity[0])
	form.addInflowCondition(Data.inflowSpatialFilters[0],inflowVelocity)
	form.addOutflowCondition(Data.outflowSpatialFilters[0])
	wallBuilding = Data.inflowSpatialFilters[0] | Data.outflowSpatialFilters[0]

	for i in range(1, Data.inflowCond):
		wallBuilding = wallBuilding | Data.inflowSpatialFilters[i]
		inflowVelocity = Function.vectorize(Data.inflowXVelocity[i], Data.inflowYVelocity[i])
		form.addInflowCondition(Data.inflowSpatialFilters[i], inflowVelocity)

	for i in range(1, Data.outflowCond):
		form.addOutflowCondition(Data.outflowSpatialFilters[i])
		wallBuilding = wallBuilding | Data.outflowSpatialFilters[i]

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

	perCellError = form.solution().energyErrorPerCell()
	return form


def solveStokesTransient():
	spaceDim = 2
	useConformingTraces = False
	mu = 1.0

	dims = [Data.xdim,Data.ydim]
	numElements = [int(Data.xelem),int(Data.yelem)]
	x0 = [0.,0.]
		#polyorder
	meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
	delta_k = 1

	transient = True
	dt = 0.1
	totalTime = 1.0
	numTimeSteps = int(totalTime / dt)
	transientForm = StokesVGPFormulation(spaceDim,useConformingTraces,mu,transient,dt)

	timeRamp = TimeRamp.timeRamp(transientForm.getTimeFunction(),1.0)

	transientForm.initializeSolution(meshTopo,int(Data.polyOrder),delta_k)

	transientForm.addZeroMeanPressureCondition()



	inflowVelocity = Function.vectorize(Data.inflowXVelocity[0], Data.inflowYVelocity[0])
	transientForm.addInflowCondition(Data.inflowSpatialFilters[0],inflowVelocity)
	transientForm.addOutflowCondition(Data.outflowSpatialFilters[0])
	wallBuilding = Data.inflowSpatialFilters[0] | Data.outflowSpatialFilters[0]

	for i in range(1, Data.inflowCond):
		wallBuilding = wallBuilding | Data.inflowSpatialFilters[i]
		inflowVelocity = Function.vectorize(Data.inflowXVelocity[i], Data.inflowYVelocity[i])
		transientForm.addInflowCondition(Data.inflowSpatialFilters[i], inflowVelocity)

	for i in range(1, Data.outflowCond):
		transientForm.addOutflowCondition(Data.outflowSpatialFilters[i])
		wallBuilding = wallBuilding | Data.outflowSpatialFilters[i]

	wall = SpatialFilter.negatedFilter(wallBuilding)
	transientForm.addWallCondition(wall)



	transientExporter = HDF5Exporter(transientForm.solution().mesh(), "transientStokes", ".")

	for timeStepNumber in range(numTimeSteps):
		transientForm.solve()
		transientExporter.exportSolution(transientForm.solution(),transientForm.getTime())
		transientForm.takeTimeStep()
		print("Time step %i completed" % timeStepNumber)

	return transientForm







