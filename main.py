from agent_handler import client_handler
import sys
import os.path

#Program created by CuS

#PLEASE READ ME
'''
This program ain`t yours mate, you can download it and modify it however you want,
however you cannot make money without it and also if you want to use it you have to
mention the program name wherever you use it as well as you have to mention me as the
creator under the Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) license.

thanks for every person that is being honest with themselves and follows the rules,
now for the technical aspects:

This is AI agent written using OOP in Python,
it uses only random and math modules so you don`t have to set the
environment except in later example use case where autosave tries to be triggered on
a specified path('ZESRaiJ\\'), which means that you need to have a folder in the same directory
with this name and give this program permission to modify the files in there and create new ones

However this AI is built different since it uses brainf**ck as it`s core and what I mean by
that is, it generates bf code.(You can either access it by looking in the folder and checking
any program generated txt file or in agent handler use:

handler.agents[agent_id].code

Thanks for reading
Have a great time reading the rest of my sh*t code

Have a nice day :)

'''
agent_amount = 50

ROM_limit = 400#chars/bytes
CPU_limit = 10 ** 3#memory cycles(how much times tried to modify/get memory data
RAM_limit = 10#amount of cells(1 byte each)
complexity = 25#amount of tests per agent per gen

path = "ZESRaiJ\\"

handler = client_handler(agent_amount, ROM_limit, CPU_limit, RAM_limit, complexity)
print("handler created")

try:
    handler.load_agents(path)
    print("agents loaded")
except:
    print("Could not load agent data")
    print("trying to set the environment")

    #check if save files exist
    for i in range(0,agent_amount):

        #if do not, create empty files
        if not os.path.isfile(path+str(i)+".txt"):
            f = open(path+str(i)+".txt","w")
            f.close()
    
    print("retrying")

    try:
        handler.load_agents(path)
    except:
        print("had problems with setting up")
        sys.exit(1)
    
while True:

    #print only every five generations
    for x in range(5):
        
        handler.mutate_generation()
        #mutate it
        last_test = handler.test_generation()
        #test generation
        handler.sort_the_agents()
        #and sort them

    handler.save_agents(path)
    #autosave

    print("max: ",max(last_test)," avr: ",sum(last_test)/len(last_test)," min: ",min(last_test))
    #print status data
