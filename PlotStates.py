# Jack Bandy
# States for selection of "plot"

from Singleton import *



@Singleton
class PromptPlot:
    def prompt(self):
        return "Yo options fo plottin now iz: u1, u2, p, stream, mesh, error"

    def getDict(self):
        return  { "u1": Plotted.Instance(),
                  "u2": Plotted.Instance(),
                  "p": Plotted.Instance(),
                  "stream": Plotted.Instance(),
                  "mesh": Plotted.Instance(),
                  "error": Plotted.Instance()
                }

    def act(self, input):
        #set the plotType so Plotted.py knows what to plot
        Data.plotType = input
        # if(input = "u1")
        return

    def isAccept(self):
        return False

    def plotu1():
      pass
      varu1 = sol.u(1);

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



@Singleton
class Plotted:
    def prompt(self):
        return 

    def getDict(self):
        return { "": Phase1.Instance() }


    def act(self, input):
        return

    def isAccept(self):
        return True

