#TestPlotClassic.py
#Jack Bandy
import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np
from numpy import *
from PyCamellia import *

spaceDim = 2
useConformingTraces = True
mu = 1.0
form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrder = 3
delta_k = 1

form.initializeSolution(meshTopo,polyOrder,delta_k)

form.addZeroMeanPressureCondition()

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)

x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)

zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

form.addWallCondition(notTopBoundary)
form.addInflowCondition(topBoundary,topVelocity)

refinementNumber = 0
form.solve()

mesh = form.solution().mesh();
u1_soln = Function.solution(form.u(1),form.solution())



#PLOT A U1
xpoints = []
ypoints = []
zvalues = []
activeCellIDs = mesh.getActiveCellIDs()
badv = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]]
for cellID in activeCellIDs:
  goodv = array(mesh.verticesForCell(cellID))
  (values,points) = u1_soln.getCellValues(mesh,cellID,badv)
  totColor = 0;
  for val in values:
    totColor += val
  for point in points:
    xpoints.append(point[0])
    ypoints.append(point[1])
  zvalues.append(totColor / len(values))

colInd = 0
xpoints = sorted(list(set(xpoints)))
ypoints = sorted(list(set(ypoints)))
cvmin = 0;
cvmax = 0;
plotColors = []
for i in range(0, (len(ypoints)-1)):
  plotColors.append([])
  for j in range(0, (len(xpoints)-1)):
    plotColors[i].append(zvalues[colInd])
    if(zvalues[colInd] < cvmin):
      cvmin = zvalues[colInd]
    if(zvalues[colInd] > cvmax):
      cvmax = zvalues[colInd]
    colInd += 1

c = plt.pcolormesh(array(xpoints), array(ypoints), array(plotColors), edgecolors='k', linewidths=2, cmap='afmhot', vmin=cvmin, vmax=cvmax) 

plt.title(' u1 ')
plt.xticks(xpoints) #x ticks are xpoints
plt.yticks(ypoints) 
plt.xlim(0, xpoints[len(xpoints)-1]) #sorted, so max = last item
plt.ylim(0, xpoints[len(xpoints)-1])
plt.show() #show the plot
