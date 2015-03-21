import re

print "Input a Regular Expression"
re = re.compile(raw_input(">> "))

while True:
    print "Enter a test input (quit to exit the program)"
    input = raw_input(">> ")
    if (input == ("quit")):
        break
    print (input == re.match(input).group()) and (input != "")

    
