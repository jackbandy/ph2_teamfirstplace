#Plot.py
#Jack Bandy
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from numpy import ma
from PyCamellia import *


spaceDim = 2
useConformingTraces = True
mu = 1.0
form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)

sol = form.solution();
loaded = Solution.load(form.bf(), "sample")


class PromptPlot:
    def prompt(self):
        return "Yo options fo plottin now iz: u1, u2, p, stream, mesh, error"

    def getDict(self):
        return 	{ "u1": Plotted.Instance(),
		  "u2": Plotted.Instance(),
		  "p": Plotted.Instance(),
		  "stream": Plotted.Instance(),
		  "mesh": Plotted.Instance(),
		  "error": Plotted.Instance()
		}


    def act(self, input):
	#set the plotType so Plotted.py knows what to plot
	Data.plotType = input
	# if input is "u1"

        return

    def isAccept(self):
        return False


    def plotu1():
      spaceDim = 2
      useConformingTraces = True
      mu = 1.0
      form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)

      sol = form.solution();
      loaded = Solution.load(form.bf(), "sample")

      varu1 = sol.u(1);
      u1_soln = Function.solution(form.u(1),form.solution())

      refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]];
      mymesh = u1_soln.mesh()
      activeCellIDs = mymesh.getActiveCellIDs()
      for cellID in activeCellIDs:
        (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        print("CellID %i:" % cellID)
        print(values)
        print(points)


    def plotu2():
      pass
      varu2 = sol.u(2);

    def plotp():
      pass
      varp = sol.p();

    def plotstream():
      pass

    def plotmesh():
      pass

    def ploterror():
      pass
