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
    
