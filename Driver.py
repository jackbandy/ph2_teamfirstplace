import re
import Phase1

print "Yo thug, you playin' PyCamellia incompressible flow solva!"

state = Phase1.Phase1.Instance()

while True:
    print state.prompt()
    input = raw_input(">> ")

    dict = state.getDict()
    parsed = input.split()
    
    #Check Every Key in the Dictionary
    for key in dict:
        m = re.compile(key);
        curr = ""

        #Check if input matches key as a Regular Expression (starting with just first word and adding words on consecutively)
        for element in parsed:
            curr += " " + element
            while curr.startswith(" "): curr = curr[1:]     #Remove spaces at start of string
            ret = m.match(curr)
            if (ret == None):
                if (input == ret.group()) and (input != ""): #curr was accepted as a key
                    state.act(curr)
                    state = dict[key] #exit Key Loop   
             
str =  m.match(input)
print (str == None)
                
           
           
