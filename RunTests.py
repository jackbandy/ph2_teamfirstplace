from ParserTests import *
import unittest


testSuite = unittest.makeSuite(ParserTests)
#testSuite.addTest(unittest.makeSuite(file name here))


testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)

