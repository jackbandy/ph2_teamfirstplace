import Data
from PyCamellia import *

class TestData(object):
    def setData(self):
	Data.Data.form = StokesVGPFormulation(Data.Data.spaceDim,Data.Data.useConformingTraces,Data.Data.mu)
	Data.Data.createOrLoad = 'create'
	Data.Data.stokesOrNS = 'stokes'
	Data.Data.reynolds = 800
	Data.Data.transientOrSS = 'transient'
	Data.Data.xdim = 2
	Data.Data.ydim = 2
	Data.Data.xelem = 2
	Data.Data.yelem = 2
	Data.Data.polyOrder = 2
	Data.Data.inflowCond = 1
	Data.Data.inflowRegion.append("x=0, y > 1")
	Data.Data.inflowXVelocity.append("-3*(y-1)*(y-2)")
	Data.Data.inflowYVelocity.append("0")
	Data.Data.outflowCond = 1
	Data.Data.outflowRegion.append("x=30")
	Data.Data.outflowXVelocity.append("")
	Data.Data.outflowYVelocity.append("")
	Data.Data.wallCond = 3
	Data.Data.wallRegion.append("x = 0, y < 1")
	Data.Data.wallRegion.append("y = 0")
	Data.Data.wallRegion.append("y=2")
	Data.Data.horp = 'h'
	Data.Data.aorm = 'auto'
	Data.Data.manualElems = ''
