from ParserTests import *
#from PlotTests import *
#from LoadSaveTests import *
#from RefineTests import *
import unittest


testSuite = unittest.makeSuite(ParserTests)
#testSuite.addTest(unittest.makeSuite(PlotTests))
#testSuite.addTest(unittest.makeSuite(TestLoadSave))
#testSuite.addTest(unittest.makeSuite(TestRefine))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)

