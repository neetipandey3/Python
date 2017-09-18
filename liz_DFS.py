import time

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

solution = input_matrix
lizards = 0
lizard_locations = []
lizards_0 = []
conflicting_positions = {(-1, -1):(-1, -1)}

#Get all the non-tree postions in a list
for col in range(size_of_nursery):
    for row in range(size_of_nursery):
        if(input_matrix[row][col] == '0'):
            lizards_0.append((row, col))

#Function to place lizard recursively on the grid
def place_lizard(solution, lizards, conflicting_positions) :
    if(lizards == no_of_lizards):
        print("Solution Found")
        return True

    for (row, col) in lizards_0:
        if(is_lizard_safe(solution, row, col, lizard_locations, conflicting_positions)):
            print("Safe move @row {} @col {}".format(row, col))
            solution[row][col] = 1
            lizard_locations.append((row, col))

            if(place_lizard(solution, lizards+1, conflicting_positions)):
                print("*******Placing lizard recrsively # {}".format(lizards))
                return True

            solution[row][col] = 0
            lizard_locations.pop()

    return False


#Function to check if the lizard is safe at the chosen row, col poistion
def is_lizard_safe(solution, new_row, new_col, lizard_locations, conflicting_positions):
    print("Lizard Loc {}".format(lizard_locations))
    temp_conflicting_pos = {(-1, -1):(-1, -1)}

    for row, col in lizard_locations:
        temp_conflicting_pos.update({(row, col): conflicting_positions[(row, col)]})

    print("List of conflicting pos {}".format(temp_conflicting_pos))

    for (row, col), pos_list in temp_conflicting_pos.items():
        if ((new_row, new_col) in pos_list or (row == new_row and col == new_col)):
            return False

    return True

#Function to get the master dictionary for all the conflicting positions with each position as the key
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

#Get the master dictionary for all the conflicting positions for each possible position on the grid
conflicting_positions = get_conflicting_positions()

if(place_lizard(solution, lizards, conflicting_positions)):
    for i in range (size_of_nursery):
        print(solution[i], sep = "")

else:
    print("FAIL")

print("Total duration = {}".format(time.time()-start_time))
