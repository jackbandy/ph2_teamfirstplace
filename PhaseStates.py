# Derek Schlabach
# States for Initial Direction to a state


from Singleton import *
import ExitStates
import SaveStates
import RefineStates
import PlotStates
import LoadStates
import CreateStates


@Singleton
class Phase1(object):

    def prompt(self):
        return "Yo options now iz: create or load."
        
    def getDict(self):
        return { "phase1": Phase1.Instance(),
                 "exit": Exit.Exit.Instance() }

    def act(self, input):
        return
        
    def isAccept(self):
        return False


@Singleton
class Phase2(object):

    def prompt(self):
        return "Yo options now iz: create, load, save, refine, plot, or exit."
        
    def getDict(self):
        return { "create" : Create.Create.Instance(), 
                 "load" : Load.Load.Instance(),
                 "save" : Save.Save.Instance(),
                 "refine" : Refine.Refine.Instance(),
                 "plot" : Plot.Plot.Instance(),
                 "exit" : Exit.Exit.Instance() }

    def act(self, input):
        return

    def isAccept(self):
        return False
