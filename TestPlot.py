#Plot.py
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
dims = [2.0,2.0]
numElements = [4,5]
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
zvals = {}
activeCellIDs = mesh.getActiveCellIDs()
cellerrs = form.solution().energyErrorPerCell()
#badv = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]]
badv = [[-1.,-1.],[-1.,0.],[-1.,1.],[0.,-1.],[0.,0.],[0.,1.],[1.,-1.],[1.,0.],[1.,1.]]

for cellID in cellerrs.keys():
  goodv = array(mesh.verticesForCell(cellID))
  zvalues.append(cellerrs[cellID])
  for point in goodv:
    xpoints.append(point[0])
    ypoints.append(point[1])
  print "testing:"
  print(zvalues)

xpoints = sorted(list(set(xpoints)))
ypoints = sorted(list(set(ypoints)))
colors = []
colInd = 0
for i in range(0, (len(ypoints)-1)):
  colors.append([])
  for j in range(0, (len(xpoints)-1)):
    colors[i].append(zvalues[colInd])
    colInd += 1

print "LENGTHS:"
print(len(xpoints))
print(len(ypoints))
cvmin = 0;
cvmax = 0;
plotColors = []
#for i in range(0, (len(ypoints)-2)):
#  plotColors.append([])
#  for j in range(0, (len(xpoints)-2)): 
#    total = 0
#    lkstr = "%d,%d" % (i*.25,j*.25)
#    total += zvals.get(lkstr)
#    lkstr = "%d,%d" % ((i+1)*.25,(j)*.25)
#    total += zvals.get(lkstr)
#    lkstr = "%d,%d" % ((i+1)*.25,(j+1)*.25)
#    total += zvals.get(lkstr)
#    lkstr = "%d,%d" % (i*.25,(j+1)*.25)
#    total += zvals.get(lkstr)
#    plotColors[i].append(total/4)
#  colInd += 1

#pcolor is known to be slower than pcolormesh

#print("Lengths: ")
#print(zvalues)
#print(xpoints)
#print(len(xpoints))
#print(len(ypoints))
#print(len(zvalues))

#print(xpoints)
#print(ypoints)
#print(zvalues)
c = plt.pcolormesh(array(xpoints), array(ypoints), array(colors), edgecolors='k', linewidths=2, cmap='afmhot', vmin=min(zvalues), vmax=max(zvalues)) 
plt.title('error')
plt.xticks(xpoints) #x ticks are xpoints
plt.yticks(ypoints)
plt.xlim(0, xpoints[len(xpoints)-1]) #sorted, so max = last item
plt.ylim(0, xpoints[len(xpoints)-1])
plt.show() #show the plot
