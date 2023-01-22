#asigning the fitness value based on all available emulator data(passed as subprocess) and inputs
def grade_the_test(test_data, subprocess):

    temp = 0

    if len(subprocess.output) == 1:

        temp = temp + 10

    if subprocess.inputs == []:

        temp = temp + 20
    
    if not subprocess.error:

        temp = temp + 50
        
    if test_data[1] in subprocess.RAM_MEMORY_CELLS:

        temp = temp + 80
        
    if test_data[1] in subprocess.output:

        temp = temp + 100
    
    #returnes the fitness value
    return temp
    
