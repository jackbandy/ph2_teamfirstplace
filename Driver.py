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
    dict = state.getDict()
    try:
        for key in dict:
            q = copy.copy(qu)
            m = re.compile(key)
            while not (len(q) == 0):
                curr = q.pop()
                ret = m.match(curr[0])
                if ret != None and curr[0] == ret.group() and curr[0] != "":
                    state.act(curr[0])
                    state = dict[key]
                    if not((len(q) == 0) or state.isAccept()):
                        state = processInput(state, curr[1])
                    return state
    except Data.ParseException:
        return state
    
    print 'Input \'' + input + '\' not understood'
    return state



# public static void main(String[] args):
def main():
    print "Welcome to the Incompressible Flow Solver!"
    state = PhaseStates.Phase1.Instance()
    startState = state
    while True:
        print state.prompt()
        if state is PhaseStates.Phase2.Instance():
            startState = state
            
            
        if not state.isAccept():
            state = processInput(state, raw_input(">> ").lower())
        else:
            try:
                state.act("")
                state = state.getDict()[""]
            except IOError:
                print 'There was an error saving or loading the file'
                state = startState
