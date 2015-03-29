from PyCamellia import *
import collections

class Data(object):
	#Initialization of form
	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
	delta_k = 1

	createOrLoad = ''
	stokesOrNS = '' # "stokes" or "navier-stokes"
	reynolds = '' #assigned a double value
	transientOrSS = '' #will be assigned value "transient" or "steady state"
	xdim = -1
	ydim = -1
	xelem = -1
	yelem = -1
	polyOrder = -1
	inflowCond = -1
	inflowRegion = []
	outflowRegion = []
	wallRegion = []
	#Queue to hold each inflow Region
	#inflowRegion.append(something) or
	#inflowRegion.popleft() 
	inflowSpatialFilters = collections.deque() #deque of spatialFilters
	inflowXVelocity = collections.deque() #deque of PyCamellia Functions
	inflowYVelocity = collections.deque() #deque of PyCamellia Functions
	outflowCond = -1
	outflowSpatialFilters = collections.deque()
	outflowXVelocity = collections.deque()
	outflowYVelocity = collections.deque()
	mesh = ''
	solution = ''

	#For Refinement
	horp = ''
	aorm = ''
	manualElems = ''

	#For communication between states.
	inflowsAskedFor = -1; #number of inflow conditions asked for and stored so far
	outflowsAskedFor = -1
	wallsAskedFor = -1

	#For save and load file names
	saveFileName = ''
	loadFileName = ''
	
	
#Exception to be raised if there's an error when parsing
class ParseException(Exception):
	def __init__(self):
		return





	
