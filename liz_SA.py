import time
import random
import math

start_time = time.time()


input_file = open("./input.txt", "r", encoding="utf-8")
method_to_use = input_file.readline()
print(method_to_use)

input_file.readline()

size_of_nursery = int(input_file.readline())
print("Size of nursery is {} X {}".format(size_of_nursery, size_of_nursery))
no_of_lizards = int(input_file.readline())
print("No of lizards = {}".format(no_of_lizards))

input_matrix = []

for _ in range(size_of_nursery):
    input_matrix.append(list(input_file.readline().strip()))
    if(len(input_matrix[-1]) != size_of_nursery):
        exit("Invalid Input")

conflicting_positions = {(-1, -1):(-1, -1)}
lizards_0 = []
solution = input_matrix

#Get a list of all non-tree positions in a list
for col in range(size_of_nursery):
    for row in range(size_of_nursery):
        if(input_matrix[row][col] == '0'):
            lizards_0.append((row, col))


#Simulated Annealing method
def solve_using_SA():
    T = 1000 #???
    delta_E = 0
    iteration = 0

    current_state = get_initial_state()
    if(get_num_conflicts(current_state) == 0):
        return current_state

    print("Current State {}".format(current_state))

    while((time.time()-start_time) <= 280):
        T = schedule(T, iteration)
        if T == 0:
            return current_state

        next_state = get_next_state(current_state)
        print("Next State {}".format(next_state))
        next_state_conflicts = get_num_conflicts(next_state)
        if(next_state_conflicts == 0):
            print("Found a solution::::: {}".format(next_state))
            return next_state
        cur_state_conflicts =  get_num_conflicts(current_state)
        delta_E =  next_state_conflicts - cur_state_conflicts
        print("Delta E {}".format(delta_E))
        P = math.exp(delta_E/T)
        print("Prob P {}".format(P))
        random_probability = random.random()
        print("Random_probability {}".format(random_probability))

        if(delta_E > 0):
            current_state = next_state
        elif(random_probability <= P):
            current_state = next_state
        iteration+=1

    return current_state

#Temperature schedule must decrease
#Need to ensure using a logarithmic division function, as we don't want T to be 0; just closer to 0
def schedule(temperature, iteration):
    #return temperature/math.log(size_of_nursery + iteration)
    return temperature - 0.0000001

#Get the initial state of lizard positions - Random
def get_initial_state():
    state = []
    liz = 0
    while( liz < no_of_lizards):
        liz_row = random.randint(0, size_of_nursery-1)
        liz_col = random.randint(0, size_of_nursery-1)
        if((liz_row, liz_col) not in state and solution[liz_row][liz_col] != '2'):
            state.append((liz_row, liz_col))
            liz+=1

    return state

#Genereate the neighbour state of lizard positions - Random??
#Move one queen alone or all the queens?
def get_next_state(current_state):
    state = []
    liz = 0

    pick_lizard = random.randint(0, size_of_nursery-1)
    while( liz < no_of_lizards):
        liz_row = random.randint(0, size_of_nursery-1)
        liz_col = random.randint(0, size_of_nursery-1)
        if((liz_row, liz_col) not in state and solution[liz_row][liz_col] != '2'):
            state.append((liz_row, liz_col))
            liz+=1

    return state

def get_num_conflicts(state):
    temp_conflicting_pos = {(-1, -1):(-1, -1)}
    conflicting_positions = get_conflicting_positions();
    no_of_conflicts = 0

    for row, col in state:
        temp_conflicting_pos.update({(row, col): conflicting_positions[(row, col)]})

    for (row, col), pos_list in temp_conflicting_pos.items():
        for (s_row, s_col) in state:
            if ((s_row, s_col) in pos_list):
                no_of_conflicts+=1

    print("Conflicts # {} in state {}".format(no_of_conflicts, state))
    return no_of_conflicts

#Get the Master dictionary for all possible conflicting positions from every position
def get_conflicting_positions():
    for row, col in lizards_0:
        temp_list = []
        rows = row+1
        while(rows <= size_of_nursery-1):
            if(solution[rows][col] == '2'):
                break
            temp_list.append((rows, col))
            rows+=1

        rows = row-1
        while(rows >= 0):
            if(solution[rows][col] == '2'):
                break
            temp_list.append((rows, col))
            rows-=1

        cols = col+1
        while(cols <= size_of_nursery-1):
            if(solution[row][cols] == '2'):
                break
            temp_list.append((row, cols))
            cols+=1

        cols = col-1
        while(cols >= 0):
            if(solution[row][cols] == '2'):
                break
            temp_list.append((row, cols))
            cols-=1

        rows = row+1
        cols = col+1
        while(rows <= size_of_nursery-1 and cols <= size_of_nursery-1):
            if(solution[rows][cols] == '2'):
                break
            temp_list.append((rows, cols))
            rows+=1
            cols+=1

        rows = row-1
        cols = col-1
        while(rows >=0 and cols >=0):
            if(solution[rows][cols] == '2'):
                break
            temp_list.append((rows, cols))
            rows-=1
            cols-=1

        rows = row-1
        cols = col+1
        while(rows >= 0 and cols <= size_of_nursery-1):
            if(solution[rows][cols] == '2'):
                break
            temp_list.append((rows, cols))
            rows-=1
            cols+=1

        rows = row-1
        cols = col+1
        while(rows >= 0 and cols <= size_of_nursery-1):
            if(solution[rows][cols] == '2'):
                break
            temp_list.append((rows, cols))
            rows-=1
            cols+=1

        conflicting_positions.update({(row, col): temp_list})
    return conflicting_positions

#Call solution function

for (row, col) in solve_using_SA():
    solution[row][col] = 1
for i in range (size_of_nursery):
    print(solution[i], sep = "")

print("Total duration = {}".format(time.time()-start_time))
