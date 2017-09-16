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


#solution = [[0]*size_of_nursery for i in range(size_of_nursery)]
solution = input_matrix

lizards = 0
lizard_locations = []

def place_lizard(solution, lizards):

    if(lizards == no_of_lizards):
        print("Solution Found")
        return True
    for col in range(size_of_nursery):
        for row in range(size_of_nursery):
            if(solution[row][col] == '2' ):
                continue
            print("Check Next move @row {} @col {}".format(row, col))
            if(is_lizard_safe(solution, row, col, lizard_locations)):
                solution[row][col] = 1
                lizard_locations.append((row, col))
                #print("No conflict @row {} @col {}".format(row, col))
                if(place_lizard(solution, lizards+1)):
                    print("*******Placing lizard # {}".format(lizards))
                    return True

                solution[row][col] = 0
                lizard_locations.pop()

    return False

#def get_lizard_locations(solution):
#    lizard_locations = []
#    for col in range(size_of_nursery):
#        for row in range(size_of_nursery):
#            if(solution[row][col] == 1):
#                lizard_locations.append((row, col))
#                print("No of lizard locations placed # {}".format(len(lizard_locations)))

#    return lizard_locations

#is lizard safe at the chosen row position in the column
def is_lizard_safe(solution, new_row, new_col, lizard_locations):
    print("Lizard Loc {}".format(lizard_locations))
    is_safe = True
    for row, col in lizard_locations:
        if(new_row == row):
            is_safe = False
            print("Same row check")
            min_col = min(col, new_col)
            max_col = max(col, new_col)
            while(min_col < max_col):
                if(solution[row][min_col] == '2'):
                    is_safe = True
                    break
                min_col+=1

            if(not is_safe):
                print("Same ROW check FAILED")
                return False

        if(new_col == col):
            is_safe = False
            print("Same col check")
            min_row = min(row, new_row)
            max_row = max(row, new_row)
            while(min_row < max_row):
                if(solution[min_row][col] == '2'):
                    is_safe = True
                    break
                min_row+=1
            if(not is_safe):
                print("Same COL check FAILED")
                return False
#check for downwards diagonal
        if(new_col - col == new_row - row):
            is_safe = False
            min_row = min(row, new_row)
            max_row = max(row, new_row)
            min_col = min(col, new_col)
            max_col = max(col, new_col)

            while(min_row <= max_row and min_col <= max_col):
                if(solution[min_row][min_col] == '2'):
                    is_safe=True
                    break
                min_row+=1
                min_col+=1
            if(not is_safe):
                return False
#check for upwards diagonal
        if(new_col - col == row - new_row):
            is_safe = False
            #min_row = min(row, new_row)
            max_row = max(row, new_row)
            min_col = min(col, new_col)
            max_col = max(col, new_col)
            while(min_col <= max_col):
                if(solution[max_row][min_col] == '2'):
                    is_safe=True
                    break
                min_col+=1
                max_row-=1
            if(not is_safe):
                return False

    return is_safe


if(place_lizard(solution, lizards)):
    for i in range (size_of_nursery):
        print(solution[i], sep = "")

else:
    print("FAIL")

print("Total duration = {}".format(time.time()-start_time))
