import random, math

#Program created by CuS

#PLEASE READ ME
'''
This program ain`t yours mate, you can download it and modify it however you want,
however you cannot make money without it and also if you want to use it you have to
mention the program name wherever you use it as well as you have to mention me as the
creator
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
#funtion used specifically for sorting agents by their key using built in sort key function
def sorter(agent):
    return agent.last_test

#this function removes a character from a string via a specified id(n)
def remove_char_by_id(string, n):
    return string[0:n]+string[n+1:]

#this function prepares and optimizes the code for the launch in emulator class
#returns list
def optimizer(code):

    #checks if code is not an empty string
    if code != "":
        compiled = [[code[0],1]]

    else:
        compiled = [["",0]]

    for i in range(1, len(code)):

        #checks if current line is loop characters(if not looks through if)
        if code[i] not in ["[","]"]:

            #if last character that it was looking at is the same it increases the amount of times the command needs to be triggered
            if compiled[len(compiled)-1][0] == code[i]:
                compiled[len(compiled)-1][1] += 1

            #if not it creates a slot for a new command
            else:
                compiled.append([code[i],1])
                
        #if loop than create a new line of a compiled code for it
        else:
            compiled.append([code[i],1])
            
    return compiled

def create_test():

    #function for creating an AI test called later by agent
    #you can manipulate it however you want to
    var1 = random.randint(0,10)
    var2 = random.randint(0,10)
    
    return [[var1, var2], var1*var2]


#asigning the fitness value based on all available emulator data(passed as subprocess) and inputs
def grade_the_test(test_data, subprocess):

    temp = 0

    if len(subprocess.output) == 1:

        temp = temp + 1

    if test_data[1] in subprocess.RAM_MEMORY_CELLS:

        temp = temp + 10
        
    if test_data[1] in subprocess.output:

        temp = temp + 100

    #returnes the fitness value
    return temp
    
class agent:

    def __init__(self, agent_id, ROM_limit, CPU_limit, RAM_limit):

        self.id = agent_id

        self.ROM_limit = ROM_limit
        self.CPU_limit = CPU_limit
        self.RAM_limit = RAM_limit

        self.last_test = None
        
        self.code = ""
        #setting local angent variables
    
    def mutate(self):

        option = random.choice(["delete", "create"])
        #choosing wheter to delete something from the current generation or add something new

        #idk dont want to explaint the mutation logic even I do not understand it fully it is complicated
        #but here is a short summary
        #first we pick delete or create something new
        #then we either pick what to delete or what new thing we wanna put in
        #after that if we choose to delete not a loop it just gets deleted but if it wants to delete a loop we look for the needed bracket
        #to either open the loop or close it so the code is going to have no bugs(syntax ones)
        #if we choose to add something we just add it somewhere and if it is a loop we add the closing bracket later on
        if option == "delete" and self.code != "":

                length = len(self.code)
                the_point = random.randint(0, length - 1)

                if self.code[the_point] not in ["[","]"]:
                    self.code = remove_char_by_id(self.code, the_point)

                elif self.code[the_point] == "]":
                    
                    list_of_openers = []

                    for i in range(0,the_point):
                        if self.code[i] == "[":
                            list_of_openers.append(i)

                    second_half = list_of_openers[len(list_of_openers)-1]

                    self.code = remove_char_by_id(self.code, the_point)
                    self.code = remove_char_by_id(self.code, second_half)
                    
                elif self.code[the_point] == "[":
                    
                    list_of_closers = []

                    for i in range(the_point, length):
                        if self.code[i] == "]":
                            list_of_closers.append(i)

                    second_half = list_of_closers[0]

                    self.code = remove_char_by_id(self.code, second_half)
                    self.code = remove_char_by_id(self.code, the_point)
                    
        elif option == "create":

                typ_mutacji = random.choice(["+","-",".",",",">","<","loop","loop"])

                if typ_mutacji != "loop":

                    point = random.randint(0,len(self.code))

                    if point not in [0, len(self.code)]:
                        self.code = self.code[0:point] + typ_mutacji + self.code[point: len(self.code)]

                    elif point == 0:
                        self.code = typ_mutacji + self.code

                    elif point == len(self.code):
                        self.code = self.code + typ_mutacji

                elif typ_mutacji == "loop" and len(self.code) > 3:


                    starting_point = random.randint(0,len(self.code)-1)
                    ending_point = random.randint(starting_point+1,len(self.code))

                    self.code = self.code[0:starting_point] + "[" + self.code[starting_point:ending_point] + "]" + self.code[ending_point:len(self.code)]
                    
                    pass

        else:
            pass

    #try to launch the agent code
    def launch(self, inputs):

        #checks if the code is to long
        if len(self.code) <= self.ROM_limit:

            #compiles the script
            compiled = optimizer(self.code)

            #creates the subprocess for the agent
            subprocess = emulator(compiled, inputs, self.CPU_limit, self.RAM_limit)


            #try except just to make sure everything works properly
            try:
                output = subprocess.run()

            except:
                #if an error was catched returns the only error message (U DUMB)
                return "U DUMB"

            #returns the emulator subprocess class
            return subprocess

        #if the code is to long also returns the error message
        else:
            return "U DUMB"
        
    def test_agent(self, test_packet):

        outputs = []
        #defines the list for scores for the agent

        #for for all the items in test packet given to the agent
        for test in test_packet:

            #gets the subprocess data by trying to launch the code
            subprocess = self.launch(test[0])

            #checks if it did not crash or get stopped for using to much power
            if subprocess != "U DUMB":
                outputs.append(grade_the_test(test, subprocess))
                #if everything went well it tries to assign a fitness value for this one test
                #in other case it gives 0 points
            else:
                outputs.append(0)

        #gets average of all the tests    
        self.last_test = sum(outputs) / len(outputs)

        #returns the average
        return self.last_test
        
class emulator:

    #sets environment variables and creates all the RAM cells
    def __init__(self, code, inputs, CPU_limit, RAM_limit):

        self.code = code
        self.inputs = inputs

        self.CPU_limit = CPU_limit
        self.RAM_limit = RAM_limit
        
        self.RAM_MEMORY_CELLS = [0 for item in range(self.RAM_limit)]

        self.USED_cycles = 0

    #this function is being triggered every time any command is an it is being used for determining wheter
    #agent used to much CPU power or not(blocks soft locking by false feedback loops)
    def one_cycle(self):

        self.USED_cycles += 1

        return self.USED_cycles > self.CPU_limit

    #returns exception code(I know, I am very creative)
    def raise_exception(self):

        return "U DUMB"

    #Increments the cell by a specified amount
    def add(self,amount):

        self.RAM_MEMORY_CELLS[self.currently_looking_at_cell] += amount

        return self.one_cycle()
    
    #Decrements the cell by a specified amount
    def substract(self, amount):

        self.RAM_MEMORY_CELLS[self.currently_looking_at_cell] -= amount

        return self.one_cycle()

    #moves the pointer to the right(cells id increases); by a specified amount
    def move_right(self, amount):
        
        self.currently_looking_at_cell += amount

        if self.currently_looking_at_cell > self.RAM_limit:
            return True

        else:
            return self.one_cycle()
        
    #moves the pointer to the left(cells id decreases); by a specified amount   
    def move_left(self, amount):

        self.currently_looking_at_cell -= amount

        if self.currently_looking_at_cell < 0:
            return True

        else:
            return self.one_cycle()

    #saves the output for the console, specified amount of times
    def console_log(self, amount):

        for i in range(amount):
            self.output.append(self.RAM_MEMORY_CELLS[self.currently_looking_at_cell])

        return self.one_cycle()

    #overwrites the cell with a first unused input line
    def input(self, amount):

        for i in range(amount):

            if self.inputs != []:
                temp = self.inputs[0]
                self.inputs.pop(0)

                self.RAM_MEMORY_CELLS[self.currently_looking_at_cell] = temp

            else:
                return self.raise_exception()
            
        return self.one_cycle()

    #Starts loop process,
    #if RAM_MEMORY[POINTER] == 0 then it moves to the next ending bracket
    #else it saves the brackets id in a list
    def loop_start(self):

        if self.RAM_MEMORY_CELLS[self.currently_looking_at_cell] != 0:
            self.loops.append(self.currently_looking_at_line)

        else:

            while self.code[self.currently_looking_at_line][0] != "]":

                self.currently_looking_at_line += 1

        return self.one_cycle()

    #if RAM_MEMORY[POINTER] == 0 then it just removes the last item from the loops array
    #else it moves the brackets specified location
    def loop_end(self):

        if self.RAM_MEMORY_CELLS[self.currently_looking_at_cell] == 0:

            self.loops.pop(len(self.loops)-1)

        else:

            self.currently_looking_at_line = self.loops[len(self.loops)-1]

        return self.one_cycle()

    #Main loop of the emulator
    def run(self):

        self.currently_looking_at_line = 0
        self.currently_looking_at_cell = 0

        self.loops = []
            
        self.output = []
        #specified env variables

        #until the code does not finish
        while self.currently_looking_at_line < len(self.code):

            #load in the command
            item = self.code[self.currently_looking_at_line]
            exception = False

            #search for the command(older python versions does not have match case)
            if item[0] == "+":
                exception = self.add(item[1])

            elif item[0] == "-":
                exception = self.substract(item[1])
                
            elif item[0] == ">":
                exception = self.move_right(item[1])

            elif item[0] == "<":
                exception = self.move_left(item[1])

            elif item[0] == ".":
                exception = self.console_log(item[1])

            elif item[0] == ",":
                exception = self.input(item[1])

            elif item[0] == "[":
                exception = self.loop_start()
                    
            elif item[0] == "]":
                exception = self.loop_end()

            #if something fricked up goes out of the main loop and returns the exception value(U DUMB)
            if exception:
                return self.raise_exception()

            #go to the next line of code    
            self.currently_looking_at_line += 1

        #returns output array(all the outputed lines for the console)
        return self.output
        
class client_handler:

    #prepares agents for work by creating them and setting environment variables
    #complexity: how much test packets you wanna perform
    #agents_amount: how much agents you need for work(i use 50)
    #ROM_limit: how long the code can be(how much characters it can use)
    #CPU_limit: how many "CPU CYCLES" the proccess can use(mostly used to avoid soft locking
    #RAM_limit: how much memory cells do you wanna give to every agent
    def __init__(self,agents_amount,ROM_limit, CPU_limit, RAM_limit, complexity):

        self.agents_amount = agents_amount

        self.ROM_limit = ROM_limit
        self.CPU_limit = CPU_limit
        self.RAM_limit = RAM_limit

        self.complexity = complexity
        
        self.agents = [ agent(id_number, self.ROM_limit, self.CPU_limit, self. RAM_limit) for id_number in range(agents_amount) ] 

    #triggers the mutate function for agents that are not top 25%
    def mutate_generation(self):

        for i in range(math.ceil((self.agents_amount / 4) * 3)):
            self.agents[i].mutate()

    #grades all the agents at the same time(by first creating a random packet) and then using the test_agent function from the agent class
    def test_generation(self):

        packet = [create_test() for i in range(self.complexity)]
        test_outputs = [agent.test_agent(packet) for agent in self.agents]

        return test_outputs

    #sorts the agents by the firtness value, usess sorter function to do that
    #later on it deletes the bottom 50% and copies the top 50% to merge those togheter
    def sort_the_agents(self):

        self.agents.sort(key=sorter)

        self.agents = self.agents[self.agents_amount//2:self.agents_amount]
        kopie = []

        for item in self.agents:
            kopie.append(agent(item.id, item.ROM_limit, item.CPU_limit, item.RAM_limit))
            kopie[len(kopie)-1].code = item.code
            
        self.agents = self.agents + kopie

    #saves all the agents data in a specified folder
    def save_agents(self, path):

        for i in range(0, len(self.agents)):
            f = open(path+str(i)+".txt","w")
            f.write(self.agents[i].code)
            f.close()

    #loads all the agents data from a folder
    def load_agents(self,path):

        for i in range(0, self.agents_amount):

            f = open(path+str(i)+".txt","r")
            dane = f.read()
            f.close()

            self.agents[i].code = dane

handler = client_handler(50, 400, 10**3, 10, 25)
print("handler created")

handler.load_agents("ZESRaiJ\\")
print("agents loaded")

while True:

    #print only every five generations
    for x in range(5):
        
        handler.mutate_generation()
        #mutate it
        last_test = handler.test_generation()
        #test generation
        handler.sort_the_agents()
        #and sort them

    handler.save_agents("ZESRaiJ\\")
    #autosave

    print("max: ",max(last_test)," avr: ",sum(last_test)/len(last_test)," min: ",min(last_test))
    #print status data
