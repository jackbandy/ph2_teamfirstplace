from Singleton import *
import Queue
from PyCamellia import *

@Singleton
class Data(object):
	#Initialization of form
	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)

	createOrLoad = ''
	stokesOrNS = ''
	reynolds = ''
	transientOrSS = ''
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
	
	
	
