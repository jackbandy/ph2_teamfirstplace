# Derek Schlabach
# States for Initial Direction to a state


from Singleton import *
import ExitStates
import SaveStates
import RefineStates
import PlotStates
import LoadStates
#import CreateStates


@Singleton
class Phase1(object):

    def prompt(self):
        return "Your options now are: create, load, and exit."
        
    def getDict(self):
        return { #"create" : CreateStates.Create.Instance(),
                 "load" : LoadStates.Load.Instance(),
                 "exit": ExitStates.Exit.Instance() }

    def act(self, input):
        return
        
    def isAccept(self):
        return False


@Singleton
class Phase2(object):

    def prompt(self):
        return "Your options now are: create, load, save, refine, plot, or exit."
        
    def getDict(self):
        return { #"create" : CreateStates.Create.Instance(), 
                 "load" : LoadStates.Load.Instance(),
                 "save" : SaveStates.Save.Instance(),
                 "refine" : RefineStates.Refine.Instance(),
                 #"plot" : PlotStates.Plot.Instance(),
                 "exit" : ExitStates.Exit.Instance() }

    def act(self, input):
        return

    def isAccept(self):
        return False
