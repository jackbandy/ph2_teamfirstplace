from Singleton import *
import Load

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
