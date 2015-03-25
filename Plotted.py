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


class Plot:
    def prompt(self):
        return

    def getDict(self):
        return { "": Phase1.Instance() }


    def act(self, input):
        return

    def isAccept(self):
        return True

