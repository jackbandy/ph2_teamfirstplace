import Queue
from PyCamellia import *

class Data(object):
	#Initialization of form
	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)

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
	#inflowRegion.put(something) or
	#inflowRegion.get() 
	inflowRegion = Queue.Queue()
	inflowXVelocity = Queue.Queue()
	inflowYVelocity = Queue.Queue()
	outflowCond = -1
	outflowRegion = Queue.Queue()
	outflowXVelocity = Queue.Queue()
	outflowYVelocity = Queue.Queue()
	wallCond = -1
	wallRegion = Queue.Queue()
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
	
	
#Exception to be raised if there's an error when parsing
class ParseException(Exception):
	def__init__(self):
		return





	
