import re
import PhaseStates
import ExitStates


def processInput(state, input):
    while input.startswith(" "): input = input[1:]    #trim whitespace from beginning
    while input.endswith(" "): input = input[:-1]     #trim whitespace from end
    dict = state.getDict()
    parsed = input.split()
   
    #Check Every Key in the Dictionary
    for key in dict:
        m = re.compile(key);
        curr = ""

        #Check if input matches key as a Regular Expression (starting with just first word and adding words on consecutively)
        i = 0 
        while i < len(parsed):
            curr += " " + parsed[i]
            while curr.startswith(" "): curr = curr[1:]    #trim whitespace from beginning
            ret = m.match(curr)
            if (ret != None):
                if (curr == ret.group()) and (curr != ""): #curr was accepted as a key
                    state.act(curr)
                    state = dict[key] #exit Key Loop
                    if state == Exit.Exit.Instance():
                        return state
                    i += 1
                    if i < len(parsed) and not state.isAccept():  #There is more input left
                        newInput = ""
                        while i < len(parsed):
                            newInput += " " + parsed[i]
                            i += 1
                        state = processInput(state, newInput)
                    return state
            i += 1

    return state

                
                    




print "Yo thug, you playin' PyCamellia incompressible flow solva!"

state = Phase1.Phase1.Instance()

while True:
    print state.prompt()
    if not state.isAccept():
        state = processInput(state, raw_input(">> "))
    else:
        state.act("")
        state = state.getDict()[""]
