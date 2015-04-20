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
import PhaseStates
import RobertsPlotter

@Singleton
class PromptPlot(object):

    plotType = ''
    def prompt(self):
        return "Options for plotting now are: u1, u2, p, stream, mesh, error"

    def getDict(self):
        return  { "0u1": Plotted.Instance(),
                  "1u2": Plotted.Instance(),
                  "2p": Plotted.Instance(),
                  "3stream": Plotted.Instance(),
                  "4mesh": Plotted.Instance(),
                  "5error": Plotted.Instance()
                }

    def act(self, input):
	#td = TestData.TestData()
	#td.setData()
	form = Data.Data().form

        print "input is: " + input
        if input == "u1":
	  plotType = 'u1'
	  plt_soln = Function.solution(form.u(1),form.solution()) 
	  RobertsPlotter.plotFunction(plt_soln,form.solution().mesh(),input)
# 	  self.plotstd(plt_soln)
        if input == "u2":
	  plotType = 'u2'
	  plt_soln = Function.solution(form.u(2),form.solution()) 
	  RobertsPlotter.plotFunction(plt_soln,form.solution().mesh(),input)
# 	  self.plotstd(plt_soln)
        if input == "p": 
	  plotType = 'p'
	  plt_soln = Function.solution(form.p(),form.solution()) 
	  RobertsPlotter.plotFunction(plt_soln,form.solution().mesh(),input)
#  	  self.plotstd(plt_soln)
        if input == "stream":
	  plotType = 'Sream'
	  form.solve()
	  stream = form.streamSolution()
	  stream.solve()
	  plt_soln = Function.solution(form.streamPhi(),stream) 
	  RobertsPlotter.plotFunction(plt_soln,stream.mesh(),input)
#	  self.plotstd(plt_soln)
        if input == "mesh":
	  plotType = 'Mesh'
	  self.plotmesh()
        if input == "error":
	  if (Data.Data.stokesOrNS is 'stokes'):
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
	cellerrs = Data.Data.form.solution().energyErrorPerCell()
	mesh = Data.Data().form.solution().mesh()
	
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
        return { "0": PhaseStates.Phase2.Instance() }

    def act(self, input):
        return

    def isAccept(self):
        return True


