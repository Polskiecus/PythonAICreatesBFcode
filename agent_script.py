import random
from interpreter import emulator, optimizer
from grades import grade_the_test

#this function removes a character from a string via a specified id(n)
def remove_char_by_id(string, n):
    return string[0:n]+string[n+1:]


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
