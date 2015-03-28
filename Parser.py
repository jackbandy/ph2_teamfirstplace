from Singleton import *
import re # regular expressions
import atexit # allows graceful quit on Ctrl-D
from PyCamellia import *
import Data

#we will never evaluate things without them being functions in Camellia
@Singleton
class ExponentEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    runTotal = 1
    exponent = int(rightOperand.evaluate(0))
    if exponent != rightOperand.evaluate(0):
      print('This program only supports integer exponents')
      raise Data.ParseException()
    for i in range(0, exponent):
      runTotal = runTotal*leftOperand
    return runTotal
    
@Singleton
class TimesEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
      return leftOperand*rightOperand
      

@Singleton
class DivideEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return leftOperand/rightOperand

@Singleton
class PlusEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return leftOperand+rightOperand
  def evaluateUnary(self, rightOperand):
    return rightOperand

@Singleton
class MinusEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return leftOperand-rightOperand
  def evaluateUnary(self, rightOperand):
    return -1*rightOperand

class InteriorExpressionParser(object):
  # set up class-level rules for operator precedence and association of operators with
  # evaluation classes
  operatorPrecedence = ['^','*','/','+','+-','-']
  operatorEvaluators = {'^' : ExponentEvaluator.Instance(),
                        '*' : TimesEvaluator.Instance(),
			'/' : DivideEvaluator.Instance(),
                        '+' : PlusEvaluator.Instance(),
			'+-' : MinusEvaluator.Instance(),
                        '-' : MinusEvaluator.Instance()}
  @staticmethod
  def isFunction(stringToken):
    return type(stringToken)==type(Function.xn())

#must return a StringRepresentation
  @staticmethod
  def parseString(interiorStringRep):
    # the definition of an interiorStringRep is one that has no parentheses in it
    tokenList = interiorStringRep
    for op in InteriorExpressionParser.operatorPrecedence:
      reducedTokenList = []
      opEvaluator = InteriorExpressionParser.operatorEvaluators[op]
      while len(tokenList) > 0:
        token = tokenList.pop(0) # get the next entry in the list
        if token == op:
          rightOperand = tokenList.pop(0) # next entry; should be a number
          # apply op to left and right operands
          if len(reducedTokenList) > 0 and InteriorExpressionParser.isFunction(reducedTokenList[-1]):
            leftOperand = reducedTokenList.pop() # last entry in reducedTokenList is our left operand
            value = opEvaluator.evaluate(leftOperand,rightOperand)
          else:
            value = opEvaluator.evaluateUnary(rightOperand)
          reducedTokenList.append(value)
        else:
          #keep this token as is, for now
          reducedTokenList.append(token)
      tokenList = reducedTokenList
    if len(tokenList) == 1:
      return tokenList[0]
    else:
      raise SyntaxError("Extra tokens remain!")
      
# Rules:
# Only enter Middle state if we have some ('s on the stack.
@Singleton
class TopLevelState(object):
  def readChar(self, parenStack, interiorStringRepStack, char):
    if char == '(':
      # add to the stack
      parenStack.append('(')
      interiorStringRepStack.append([])
      return MiddleState.Instance()
    elif char == ')':
      # from Accept state, getting a close paren means Reject
      print("Unbalanced parentheses")
      raise Data.ParseException()
      return RejectState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorStringRep
      interiorStringRepStack[-1].append(char)
      return TopLevelState.Instance()
  def __str__(self):
    return "TopLevel"

@Singleton
class MiddleState(object):
  def readChar(self, parenStack, interiorStringRepStack, char):
    if char == '(':
      # add to the stacks
      parenStack.append('(')
      interiorStringRepStack.append([])
      return MiddleState.Instance()
    elif char == ')':
      # according to our Rule, if we are in MiddleState, something is on stack
      parenStack.pop()
      # it's time to convert the interiorStringRep to a numerical value,
      # and to append that to the interiorStringRep on the stack level above us
      interiorStringRep = interiorStringRepStack.pop() # get last entry, and remove from stack
      #print ("evaluating interiorStringRep: " + interiorStringRep)
      value = InteriorExpressionParser.parseString(interiorStringRep)
      #print ("value after close parenthesis: " + str(value))
      interiorStringRepStack[-1].append(value)
      # if there is something left on the stack, we remain in Middle state;
      # otherwise, we have closed the last paren, and we can return to TopLevel
      if len(parenStack) == 0:
        return TopLevelState.Instance()
      else:
        return MiddleState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorStringRep
      interiorStringRepStack[-1].append(char)
      return MiddleState.Instance()
  def __str__(self):
    return "Middle"
  
@Singleton
class RejectState(object):
  def readChar(self, parenStack, interiorStringRepStack, char):
    #Once we are in Reject state, we stay there:
    return RejectState.Instance()
  def __str__(self):
    return "Reject"

class StateMachine(object):
  def __init__(self):
    self.stack = []
    self.interiorStringRepStack = [[]]
    self.state = TopLevelState.Instance()

  def readString(self, inputString):
    # make all things like 3(4+2) into 2*(4+2)
#    inputString = inputString.lower()
#    inputString = "".join(inputString.split())
#    inputString = re.split('([0-9]*\.[0-9]+|[0-9]+|[a-z]+|\(|\))',inputString)
    







    functionPtrArrayAndOps = self.makeFunctionPtrs(inputString)
    for i in range(0, len(functionPtrArrayAndOps)):
      self.readElement(functionPtrArrayAndOps[i])  

  def makeFunctionPtrs(self, inputString):
    # First make everything in the string into a functionPtr
      inputString = inputString.lower()
      inputString = "".join(inputString.split())
      #note that inputString is no longer a string technically. It is an array of strings
      inputString = re.split('([0-9]*\.[0-9]+|[0-9]+|[a-z]+|\(|\))',inputString)
      #remove blank elements
      inputString = [i for i in inputString if i != '']
      reNum = re.compile('([0-9]*\.[0-9]+|[0-9]+)')
      reVar = re.compile('[a-z]+')
      keys = []
      for i in range(0, len(inputString)):
        reNumMatch = reNum.match(inputString[i])
        reVarMatch = reVar.match(inputString[i])
        #if the inputString[i] is a number
        if (reNumMatch != None and inputString[i] == reNumMatch.group()):
          inputString[i] = Function.constant(float(inputString[i]))
        #if inputString[i] is a variable.
        elif (reVarMatch != None and inputString[i] == reVarMatch.group()):
	  # if j ==0 then keys is empty, and we must store this string
          if len(keys)==0:
            keys.append(inputString[i])
            inputString[i] = Function.xn(1)
          #if this fires then we have already ran into this variable
          elif keys[0] == inputString[i]:
            inputString[i] = Function.xn(1)
          #if j == 1 then keys has one variable in it
          elif len(keys)>=1:
            print('Only one variable is able to be used in the function')
            raise Data.ParseException()
      return inputString

  def readElement(self, element):
    #try:
    self.state = self.state.readChar(self.stack, self.interiorStringRepStack, element)
    #except:
      #print("Rejecting due to exception caught in StateMachine.")
    #self.state = RejectState.Instance()
    #print(self.state)
  def isInAcceptState(self):
    return self.state is TopLevelState.Instance()
  def value(self):
    if self.isInAcceptState() and len(self.interiorStringRepStack) == 1:
      topLevelString = self.interiorStringRepStack[0]
      return InteriorExpressionParser.parseString(topLevelString)
    else:
      raise SyntaxError("Not in accept state")

def quitGracefully():
  print("\nGoodbye!")

atexit.register(quitGracefully)

@Singleton
class Parser(object):

  def parse(self, inputString):
    stateMachine = StateMachine()
    try:
      stateMachine.readString(inputString)
      value = stateMachine.value()
      return value
    except:
      raise Data.ParseException
