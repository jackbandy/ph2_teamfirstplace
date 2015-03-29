# PhaseStates.py
# Derek Schlabach
# States for Initial Direction to a state


from Singleton import *
import SaveStates, RefineStates, PlotStates, LoadStates, CreateStates


@Singleton
class Phase1(object):

    def prompt(self):
        return "Your options now are: create and load."
        
    def getDict(self):
        return { "0create" : CreateStates.Create.Instance(),
                 "1load" : LoadStates.Load.Instance(), }

    def act(self, input):
        return
        
    def isAccept(self):
        return False


@Singleton
class Phase2(object):

    def prompt(self):
        return "Your options now are: create, load, save, refine, or plot."
        
    def getDict(self):
        return { "0create" : CreateStates.Create.Instance(), 
                 "1load" : LoadStates.Load.Instance(),
                 "2save" : SaveStates.Save.Instance(),
                 "3refine" : RefineStates.Refine.Instance(),
                 "4plot" : PlotStates.PromptPlot.Instance(), }

    def act(self, input):
        return

    def isAccept(self):
        return False
