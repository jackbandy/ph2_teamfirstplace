from Parser import *
import re # regular expressions
from PyCamellia import *
import unittest
from IntegerExpressionParser import *


class ParserTests(unittest.TestCase):
	parser = RobertsParser.Instance()
	def testParseInts(self):
		self.assertEqual((ParserTests.parser).parse("3+3"), 6)
	def testParseWhiteSpace(self):
		self.assertEqual(ParserTests.parser.parse(" 3 + 3 "), 6)
	def testParseDoubles(self):
		self.assertEqual(ParserTests.parser.parse("3.3+3"), 6.3)
	def testParseDivideInts(self):
		self.assertEqual(ParserTests.parser.parse("9/3"), 3)
	def testParsePlusNegative(self):
		self.assertEqual(ParserTests.parser.parse("9+-3"), 6)
	def testDivideDoubles(self):
		self.assertEqual(ParserTests.parser.parse("5/2"), 2.5)
	def testParseWithParen(self):
		self.assertEqual(ParserTests.parser.parse("(5+3)*3"), 24)
	


if (__name__ == '__main__'):
  unittest.main()


	
