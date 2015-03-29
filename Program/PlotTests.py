# PlotTests.py
# Jack Bandy

import unittest
import PlotStates
import TestData
import Data
from PyCamellia import *


class PlotTests(unittest.TestCase):
  '''Test Things'''

  td = TestData.TestData()
  td.setData()
#  def testu1(self):
#    PlotStates.PromptPlot.Instance().act("u1")
#  def testu2(self):
#    PlotStates.PromptPlot.Instance().act("u2")
#  def testp(self):
#    PlotStates.PromptPlot.Instance().act("p")
#  def teststream(self):
#    PlotStates.PromptPlot.Instance().act("stream")
  def testmesh(self):
    PlotStates.PromptPlot.Instance().act("mesh")
#  def testerror(self):
#    PlotStates.PromptPlot.Instance().act("error")

# Run the tests:
if (__name__ == '__main__'):
  unittest.main()
