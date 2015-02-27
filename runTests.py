from PyCamellia import *
import unittest

testSuite = unittest.makeSuite(TestSuite.py)
#testSuite.addTest(unittest.makeSuite(something))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
