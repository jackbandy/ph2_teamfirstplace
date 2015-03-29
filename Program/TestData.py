import Data
from PyCamellia import *

class TestData(object):
    def setData(self):
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
	Data.Data.horp = 'h'
	Data.Data.aorm = 'auto'
	Data.Data.manualElems = ''
	Data.Data.form = StokesVGPFormulation(Data.Data.spaceDim,Data.Data.useConformingTraces,Data.Data.mu)

	# Required initialization
	dims = [2.0,2.0]
        numElements = [4,5]
        x0 = [0.,0.]
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        polyOrder = 3
        delta_k = 1
        Data.Data.form.initializeSolution(meshTopo,polyOrder,delta_k)
        Data.Data.form.addZeroMeanPressureCondition()
        topBoundary = SpatialFilter.matchingY(1.0)
        notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
        x = Function.xn(1)
        rampWidth = 1./64
        H_left = Function.heaviside(rampWidth)
        H_right = Function.heaviside(1.0-rampWidth);
        ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
        zero = Function.constant(0)
        topVelocity = Function.vectorize(ramp,zero)
        Data.Data.form.addWallCondition(notTopBoundary)
        Data.Data.form.addInflowCondition(topBoundary,topVelocity)
        refinementNumber = 0
        Data.Data.form.solve()
