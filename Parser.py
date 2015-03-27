from Singleton import *
import re # regular expressions
import atexit # allows graceful quit on Ctrl-D
from PyCamellia import *

#we will never evaluate things without them being functions in Camellia

@Singleton
class ExponentEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return float(leftOperand)**float(rightOperand)
    
@Singleton
class TimesEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return float(leftOperand)*float(rightOperand)

@Singleton
class DivideEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return float(leftOperand)/float(rightOperand)

@Singleton
class PlusEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return float(leftOperand)+float(rightOperand)
  def evaluateUnary(self, rightOperand):
    return float(rightOperand)

@Singleton
class MinusEvaluator(object):
  def evaluate(self, leftOperand, rightOperand):
    return float(leftOperand)-float(rightOperand)
  def evaluateUnary(self, rightOperand):
    return -float(rightOperand)

# x2 = Function.xn(2) x^2
# c = Function.constant(4)

class StringRepresentation(object):
  def __init__(self):
    a = 1
    self.rep = []
  def append(self, argument):
    (self.rep).append(argument)
  def pop(self, index):
    return (self.rep).pop(index)


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
  def isFloat(stringToken):
    try:
        float(stringToken)
        return True
    except ValueError:
        return False

#must return a StringRepresentation
  @staticmethod
  def parseString(interiorStringRep):
    # the definition of an interiorStringRep is one that has no parentheses in it
    # first, convert the string into a list of numbers and characters that correspond to our operators
    interiorStringRep = "".join(interiorStringRep.split())
    interiorStringRep = interiorStringRep.lower()
    tokenList = re.split('([0-9]*\.[0-9]+|[0-9]+|x|y)',interiorStringRep)
    # drop the first and last (empty string) values from the list:
    tokenList = tokenList[1:-1]
    for op in InteriorExpressionParser.operatorPrecedence:
      reducedTokenList = []
      opEvaluator = InteriorExpressionParser.operatorEvaluators[op]
      while len(tokenList) > 0:
        token = tokenList.pop(0) # get the next entry in the list
        if token == op:
          rightOperand = tokenList.pop(0) # next entry; should be a number
          # apply op to left and right operands
          if len(reducedTokenList) > 0 and InteriorExpressionParser.isFloat(reducedTokenList[-1]):
            leftOperand = reducedTokenList.pop() # last entry in reducedTokenList is our left operand
            #print("evaluating op " + op + " on (" + str(leftOperand) + ", " + str(rightOperand) + ")")
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
  def readChar(self, parenStack, interiorStringRepRepStack, char):
    if char == '(':
      # add to the stack
      parenStack.append('(')
      interiorStringRepRepStack.append(interiorStringRepRepresentation())
      return MiddleState.Instance()
    elif char == ')':
      # from Accept state, getting a close paren means Reject
      return RejectState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorStringRep
      interiorStringRepRepStack[-1].append(char)
      return TopLevelState.Instance()
  def __str__(self):
    return "TopLevel"
  

@Singleton
class MiddleState(object):
  def readChar(self, parenStack, interiorStringRepRepStack, char):
    if char == '(':
      # add to the stacks
      parenStack.append('(')
      interiorStringRepRepStack.append(interiorStringRepRepresentation())
      return MiddleState.Instance()
    elif char == ')':
      # according to our Rule, if we are in MiddleState, something is on stack
      parenStack.pop()
      # it's time to convert the interiorStringRep to a numerical value,
      # and to append that to the interiorStringRep on the stack level above us
      interiorStringRepRep = interiorStringRepRepStack.pop() # get last entry, and remove from stack
      #print ("evaluating interiorStringRep: " + interiorStringRep)
      value = InteriorExpressionParser.parseString(interiorStringRepRep)
      #print ("value after close parenthesis: " + str(value))
      interiorStringRepRepStack[-1].append(value)
      # if there is something left on the stack, we remain in Middle state;
      # otherwise, we have closed the last paren, and we can return to TopLevel
      if len(parenStack) == 0:
        return TopLevelState.Instance()
      else:
        return MiddleState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorStringRep
      interiorStringRepRepStack[-1].append(char)
      return MiddleState.Instance()
  def __str__(self):
    return "Middle"
  
@Singleton
class RejectState(object):
  def readChar(self, parenStack, interiorStringRepRepStack, char):
    #Once we are in Reject state, we stay there:
    return RejectState.Instance()
  def __str__(self):
    return "Reject"

class StateMachine(object):
  def __init__(self):
    self.stack = []
    self.interiorStringRepRepStack = [StringRepresentation()]
    self.state = TopLevelState.Instance()
  def readString(self, inputString):
      # we will delete these lines
      theInputString = inputString
      for char in theInputString:
        self.readElement(char)



      # First make everything in the string into a functionPtr
      inputString = inputString.lower()
      inputString = "".join(inputString.split())
      inputString = re.split('([0-9]*\.[0-9]+|[0-9]+|[a-z]+)',inputString)
      #remove blank elements
      inputString = [i for i in inputString if i != '']
      reNum = re.compile('([0-9]*\.[0-9]+|[0-9]+)')
      reVar = re.compile('[a-z]+')
      j = 0
      vals = ["x", "y"]
      for i in range(0, len(inputString)):
        reNumMatch = reNum.match(inputString[i])
        reVarMatch = reVar.match(inputString[i])
        #if the inputString[i] is a number
        if (reNumMatch != None and inputString[i] == reNumMatch.group()):
          inputString[i] = Function.constant(float(inputString[i]))
        #if inputString[i] is a variable
        elif (reVarMatch != None and inputString[i] == reVarMatch.group()):
          if keys[0] == inputString[i]:
            inputString[i] = Function.xn(1)
          elif keys[1] == inputString[i]:
            inputString[i] = Function.yn(1)
          elif (j>len(vals)):
            raise VariablesError('')
          elif j==0:
            keys[j] = inputString[i]
	    j=j+1
            inputString[i] = Function.xn(1)
          elif j==1:
            keys[j] = inputString[i]
	    j=j+1
            inputString[i] = Function.yn(1)
      # now everything is a function pointer
      inputStringRep = inputString

# we will add these lines
#      for i in range(0, len(inputStringRep))
#        self.readElement(inputStringRep[i])  

  def readElement(self, element):
    try:
      self.state = self.state.readChar(self.stack, self.interiorStringRepRepStack, element)
    except:
      #print("Rejecting due to exception caught in StateMachine.")
      self.state = RejectState.Instance()
    #print(self.state)
  def isInAcceptState(self):
    return self.state is TopLevelState.Instance()
  def value(self):
    if self.isInAcceptState() and len(self.interiorStringRepRepStack) == 1:
      topLevelString = self.interiorStringRepRepStack[0]
      #print("topLevelString: " + topLevelString)
      return InteriorExpressionParser.parseString(topLevelString)
    else:
      print(self.interiorStringRepRepStack)
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
      print("Syntax error: could not parse string.")
        #raise #Uncomment this to see what exception was thrown
