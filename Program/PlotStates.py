# Jack Bandy
# States for selection of "plot"

from Singleton import *
import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np
from numpy import *
from PyCamellia import *
import Data
import TestData


@Singleton
class PromptPlot(object):

    plotType = ''
    def prompt(self):
        return "Options for plotting now are: u1, u2, p, stream, mesh, error"

    def getDict(self):
        return  { "u1": Plotted.Instance(),
                  "u2": Plotted.Instance(),
                  "p": Plotted.Instance(),
                  "stream": Plotted.Instance(),
                  "mesh": Plotted.Instance(),
                  "error": Plotted.Instance()
                }

    def act(self, input):
	#td = TestData.TestData()
	#td.setData()
	form = Data.Data().form
#        dims = [2.0,2.0]
#        numElements = [4,5]
#        x0 = [0.,0.]
#        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
#        polyOrder = 3
#        delta_k = 1
#       
#        form.initializeSolution(meshTopo,polyOrder,delta_k)
#       
#        form.addZeroMeanPressureCondition()
#       
#        topBoundary = SpatialFilter.matchingY(1.0)
#        notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
#       
#        x = Function.xn(1)
#        rampWidth = 1./64
#        H_left = Function.heaviside(rampWidth)
#        H_right = Function.heaviside(1.0-rampWidth);
#        ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
#       
#        zero = Function.constant(0)
#        topVelocity = Function.vectorize(ramp,zero)
#       
#        form.addWallCondition(notTopBoundary)
#        form.addInflowCondition(topBoundary,topVelocity)
#       
#        refinementNumber = 0
#        form.solve()


        if input is "u1":
	  plotType = 'u1'
	  plt_soln = Function.solution(form.u(1),form.solution()) 
	  self.plotstd(plt_soln)
        if input is "u2":
	  plotType = 'u2'
	  plt_soln = Function.solution(form.u(2),form.solution()) 
	  self.plotstd(plt_soln)
        if input is "p": 
	  plotType = 'p'
	  plt_soln = Function.solution(form.p(),form.solution()) 
	  self.plotstd(plt_soln)
        if input is "stream":
	  plotType = 'Sream'
	  form.solve()
	  stream = form.streamSolution()
	  stream.solve()
	  plt_soln = Function.solution(form.streamPhi(),stream) 
	  self.plotstd(plt_soln)
        if input is "mesh":
	  plotType = 'Mesh'
	  self.plotmesh()
        if input is "error":
	  if (data.stokesOrNS is 'stokes'):
	    plotType = 'Stokes Error'
	    cellerrs = form.solution().energyErrorPerCell()
	    self.ploterror()
	  else:
	    plotType = 'Navier-Stokes Error'
	    cellerrs = form.solutionIncrement().energyErrorPerCell()
	    self.ploterror()


    def isAccept(self):
        return False


    def plotstd(self, plt_soln):
	mesh = Data.Data().form.solution().mesh()
	xpoints = []
	ypoints = []
	zvalues = []
	activeCellIDs = mesh.getActiveCellIDs()
	badv = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]]
	for cellID in activeCellIDs:
	  goodv = array(mesh.verticesForCell(cellID))
	  (values,points) = plt_soln.getCellValues(mesh,cellID,badv)
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
	

	print(plotColors)	
	c = plt.pcolormesh(array(xpoints), array(ypoints), array(plotColors), edgecolors='k', linewidths=2, cmap='afmhot', vmin=cvmin, vmax=cvmax)
	
	plt.title(self.plotType)
	plt.xticks(xpoints) #x ticks are xpoints
	plt.yticks(ypoints)
	plt.xlim(0, xpoints[len(xpoints)-1]) #sorted, so max = last item
	plt.ylim(0, xpoints[len(xpoints)-1])
	plt.show() #show the plot
	




    def plotmesh(self):
	mesh = Data.Data().form.solution().mesh()
	xpoints = []
        ypoints = []
        zvalues = []
        activeCellIDs = mesh.getActiveCellIDs()
        for cellID in activeCellIDs:
          goodv = mesh.verticesForCell(cellID)
          for val in values:
            totColor += val
          for point in goodv:
            xpoints.append(point[0])
            ypoints.append(point[1])
        zvalues = zeros((len(xpoints)-1, len(ypoints)-1))

        colInd = 0
        xpoints = sorted(list(set(xpoints)))
        ypoints = sorted(list(set(ypoints)))
        c = plt.pcolormesh(array(xpoints), array(ypoints), array(zvalues), edgecolors='k', linewidths=2, cmap='bwr', vmin='-100', vmax='100') 

        plt.title('Mesh')
        plt.xticks(xpoints)
        plt.yticks(ypoints)
        plt.xlim(0, xpoints[len(xpoints)-1])
        plt.ylim(0, ypoints[len(ypoints)-1])
        plt.show()


    def ploterror(self):
	xpoints = []
	ypoints = []
	zvalues = []
	cellerrs = form.solution().energyErrorPerCell()
	
	for cellID in cellerrs.keys():
	  goodv = array(mesh.verticesForCell(cellID))
	  zvalues.append(cellerrs[cellID])
	  for point in goodv:
	    xpoints.append(point[0])
	    ypoints.append(point[1])
	
	xpoints = sorted(list(set(xpoints)))
	ypoints = sorted(list(set(ypoints)))
	colors = []
	colInd = 0
	for i in range(0, (len(ypoints)-1)):
	  colors.append([])
	  for j in range(0, (len(xpoints)-1)):
	    colors[i].append(zvalues[colInd])
	    colInd += 1
	
	cvmin = 0;
	cvmax = 0;
	c = plt.pcolormesh(array(xpoints), array(ypoints), array(colors), edgecolors='k', linewidths=2, cmap='afmhot', vmin=min(zvalues), vmax=max(zvalues))
	plt.title('plotType')
	plt.xticks(xpoints) #x ticks are xpoints
	plt.yticks(ypoints)
	plt.xlim(0, xpoints[len(xpoints)-1]) #sorted, so max = last item
	plt.ylim(0, xpoints[len(xpoints)-1])
	plt.show()



@Singleton
class Plotted:
    def prompt(self):
        return 

    def getDict(self):
        return { "": PhaseStates.Phase2.Instance() }

    def act(self, input):
        return

    def isAccept(self):
        return True


