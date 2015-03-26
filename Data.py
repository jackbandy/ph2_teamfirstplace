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
	#Queue to hold each inflow Region
	#inflowRegion.append(something) or
	#inflowRegion.popleft() 
	inflowRegion = collections.deque()
	inflowXVelocity = collections.deque()
	inflowYVelocity = collections.deque()
	outflowCond = -1
	outflowRegion = collections.deque()
	outflowXVelocity = collections.deque()
	outflowYVelocity = collections.deque()
	wallCond = -1
	wallRegion = collections.deque()
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





	
