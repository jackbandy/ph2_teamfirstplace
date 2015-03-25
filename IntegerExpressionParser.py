from Singleton import *

import re # regular expressions
import atexit # allows graceful quit on Ctrl-D

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
  @staticmethod
  def parseString(interiorString):
    # the definition of an interiorString is one that has no parentheses in it
    # first, convert the string into a list of numbers and characters that correspond to our operators
    interiorString = "".join(interiorString.split())
    tokenList = re.split('([0-9]*\.[0-9]+|[0-9]+)',interiorString)
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
  def readChar(self, parenStack, interiorStringStack, char):
    if char == '(':
      # add to the stack
      parenStack.append('(')
      interiorStringStack.append('')
      return MiddleState.Instance()
    elif char == ')':
      # from Accept state, getting a close paren means Reject
      return RejectState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorString
      interiorStringStack[-1] += char
      return TopLevelState.Instance()
  def __str__(self):
    return "TopLevel"
  
@Singleton
class MiddleState(object):
  def readChar(self, parenStack, interiorStringStack, char):
    if char == '(':
      # add to the stacks
      parenStack.append('(')
      interiorStringStack.append('')
      return MiddleState.Instance()
    elif char == ')':
      # according to our Rule, if we are in MiddleState, something is on stack
      parenStack.pop()
      # it's time to convert the interiorString to a numerical value,
      # and to append that to the interiorString on the stack level above us
      interiorString = interiorStringStack.pop() # get last entry, and remove from stack
      #print ("evaluating interiorString: " + interiorString)
      value = InteriorExpressionParser.parseString(interiorString)
      #print ("value after close parenthesis: " + str(value))
      interiorStringStack[-1] += str(value)
      
      # if there is something left on the stack, we remain in Middle state;
      # otherwise, we have closed the last paren, and we can return to TopLevel
      if len(parenStack) == 0:
        return TopLevelState.Instance()
      else:
        return MiddleState.Instance()
    else:
      # for any other character, stay in the current level; append to interiorString
      interiorStringStack[-1] += char
      return MiddleState.Instance()
  def __str__(self):
    return "Middle"
  
@Singleton
class RejectState(object):
  def readChar(self, parenStack, interiorStringStack, char):
    #Once we are in Reject state, we stay there:
    return RejectState.Instance()
  def __str__(self):
    return "Reject"

class StateMachine(object):
  def __init__(self):
    self.stack = []
    self.interiorStringStack = ['']
    self.state = TopLevelState.Instance()
  def readString(self, inputString):
      for char in inputString:
        self.readChar(char)
  def readChar(self, char):
    try:
      self.state = self.state.readChar(self.stack, self.interiorStringStack, char)
    except:
      #print("Rejecting due to exception caught in StateMachine.")
      self.state = RejectState.Instance()
    #print(self.state)
  def isInAcceptState(self):
    return self.state is TopLevelState.Instance()
  def value(self):
    if self.isInAcceptState() and len(self.interiorStringStack) == 1:
      topLevelString = self.interiorStringStack[0]
      #print("topLevelString: " + topLevelString)
      return InteriorExpressionParser.parseString(topLevelString)
    else:
      print(self.interiorStringStack)
      raise SyntaxError("Not in accept state")

def quitGracefully():
  print("\nGoodbye!")

atexit.register(quitGracefully)

@Singleton
class RobertsParser(object):



  def parse(self, inputString):
    stateMachine = StateMachine()
    try:
      stateMachine.readString(inputString)
      value = stateMachine.value()
      return value
    except:
      print("Syntax error: could not parse string.")
        #raise #Uncomment this to see what exception was thrown
