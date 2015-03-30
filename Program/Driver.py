import re, copy, Data, PhaseStates, ExitStates
from collections import deque

# Remove whitespace from beginning and end of a string
def trim(str):
    while str.startswith(" "): str = str[1:]
    while str.endswith(" "): str = str[:-1]
    return str

# Chop up an input into different splices stored in a deque
# Example
# "A dog eats" => | ("A dog eats", "") |
#                 | ("A dog", "eats")  |
#                 | ("A", "dog eats")  |
def chopInput(input):
    q = deque()
    input = trim(input)
    q.appendleft((input, ""))
    i = len(input) - 1
    while i > 0:
        if (input[i] == " " and re.match('.*\S', input[:i]) and re.match('.*\S.*', input[i:])):
            q.appendleft((trim(input[:i]), trim(input[i:])))
        i -=1 
    return q
        

# Check if the input (or a correct portion of the input) is accepted by the current state
# If it is, call act() on the state and move on to the next state
def processInput(state, input):
    qu = chopInput(input)
    if input == "exit" or input == "quit":
        return ExitStates.Exit.Instance()
    newList = list()
    dict = state.getDict()
    for x in dict:
        newList.insert(int(x[0]) , x[1:])
    try:
        for key in newList:
            q = copy.copy(qu)
            m = re.compile(key)
            while not (len(q) == 0):
                curr = q.pop()
                ret = m.match(curr[0])
                if ret != None and curr[0] == ret.group() and curr[0] != "":
                    state.act(curr[0])
                    state = dict[str(newList.index(key)) + key]
                    if not((curr[1] == "") or state.isAccept()):
                        state = processInput(state, curr[1])
                    return state
    except Data.ParseException:
	print("\nSome common errors due to unsupported inputs: scientific notation (1e4) is not supported.\n Only one operator is allowed to be between two values. (E.g. 2(3+3) is not supported. Instead please enter 2*(3+3)")
        return state
    
    print 'Input \'' + input + '\' not understood'
    return state



# public static void main(String[] args):
def main():
    print "\n\n-------Welcome to the Incompressible Flow Solver-------"
    print "---To exit at any time, simply type 'quit' or 'exit'---\n"
    state = PhaseStates.Phase1.Instance()
    startState = state
    while True:

        if not state.isAccept():
            print state.prompt()
            if state is PhaseStates.Phase2.Instance():
                startState = state
            state = processInput(state, raw_input(">> ").lower())

        else:
            try:
                state.act("")
                state = state.getDict()[""]
            except IOError:
                print 'There was an error saving or loading the file'
                state = startState
