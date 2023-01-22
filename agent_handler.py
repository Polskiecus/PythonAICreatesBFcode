import math
from agent_script import agent
from tests import create_test

#funtion used specifically for sorting agents by their key using built in sort key function
def sorter(agent):
    return agent.last_test

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
