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
