#Scott Wurtz
from Parser import *
import re # regular expressions
from PyCamellia import *
import unittest


class ParserTests(unittest.TestCase):
	parser = Parser.Instance()
	def testParseInts(self):
		func = (ParserTests.parser).parse("3+3")
		self.assertEqual(func.evaluate(0), 6)
	def testParseWhiteSpace(self):
		func = ParserTests.parser.parse(" 3 + 3 ")
		self.assertEqual(func.evaluate(0), 6)
	def testParseDoubles(self):
		func = ParserTests.parser.parse("3.3+3")
		self.assertEqual(func.evaluate(0), 6.3)
	def testParseDivideInts(self):
		func = ParserTests.parser.parse("9/3")
		self.assertEqual(func.evaluate(0), 3)
	def testParsePlusNegative(self):
		func = ParserTests.parser.parse("9+-3")
		self.assertEqual(func.evaluate(0), 6)
	def testParseDivideDoubles(self):
		func = ParserTests.parser.parse("5/2")
		self.assertEqual(func.evaluate(0), 2.5)
	def testParseWithParen(self):
		func = ParserTests.parser.parse("(5+3)*3")
		self.assertEqual(func.evaluate(1,2), 24)
	def testParseWithVariables(self):
		func = ParserTests.parser.parse("3*x+2")
		self.assertEqual(func.evaluate(2), 8)
	def testParseWithJustX(self):
		func = ParserTests.parser.parse("x")
		self.assertEqual(func.evaluate(2), 2)
	def testParseWithUpperCase(self):
		func = ParserTests.parser.parse("X")
		self.assertEqual(func.evaluate(2), 2)
	def testParseWithJustParen(self):
		func = ParserTests.parser.parse("(3)")
		self.assertEqual(func.evaluate(2,3), 3)
	def testParseWithJustParen(self):
		func = ParserTests.parser.parse("(x)")
		self.assertEqual(func.evaluate(2), 2)
	def testParseWithParen2(self):
		func = ParserTests.parser.parse("(x+3)")
		self.assertEqual(func.evaluate(2), 5)
	def testParseWithParen3(self):
		func = ParserTests.parser.parse("(x+3)+3")
		self.assertEqual(func.evaluate(2), 8)
	def testParseDrRoberts3(self):
		func = ParserTests.parser.parse("-3*y*y+9*y-6")
		y = 3
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
		y = 4
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
	def testParseDrRoberts2(self):
		func = ParserTests.parser.parse("3*(1-y)*(y-2)")
		y = 3
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
		y = 4
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
	def testParseDrRoberts(self):
		func = ParserTests.parser.parse("-3*y^2+9*y-6")
		y = 3
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
		y = 4
		self.assertEqual(func.evaluate(y), -3*y**2+9*y-6)
	def testParseWithLots(self):
		func = ParserTests.parser.parse("(x+3)*4/4+3*2^2")
		self.assertEqual(func.evaluate(2), 17)
	def testParseWithExponent(self):
		func = ParserTests.parser.parse("2^3")
		self.assertEqual(func.evaluate(2), 8)

if (__name__ == '__main__'):
  unittest.main()


	
