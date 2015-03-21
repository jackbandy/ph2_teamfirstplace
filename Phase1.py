from Singleton import *
import Exit

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
