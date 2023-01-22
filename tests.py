import random

def create_test():

    #function for creating an AI test called later by agent
    #you can manipulate it however you want to
    var1 = random.randint(0,10)
    var2 = random.randint(0,10)
    
    return [[var1, var2], var1*var2]
