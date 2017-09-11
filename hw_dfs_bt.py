
input_file = open("./input.txt", "r", encoding="utf-8")
method_to_use = input_file.readline()
print(method_to_use)
size_of_nursery = int(input_file.readline())
print("Size of nursery is {} X {}".format(size_of_nursery, size_of_nursery))
no_of_lizards = int(input_file.readline())
print("No of lizards = {}".format(no_of_lizards))


#recursive for every col find a safe row
def find_solution(n):
    if(n==0):
        return [[]]
    else:
        return place_lizard(find_solution(n-1), n-1)

def place_lizard(existing_solution, next_col_move):
    solution = []
    for each_existing_path in existing_solution:
        print("Append to solution{}".format(existing_solution))
        for row in range(size_of_nursery):
            if(is_lizard_safe(each_existing_path, row, next_col_move)):
                print("Safe @ row{} column{}".format(row, next_col_move))
                solution.append(each_existing_path + [row])
    return solution


#is lizard safe at the chosen row position in the column
def is_lizard_safe(solution, selected_row, new_col):
    safe = True
    for col in range(new_col):
        if(solution[col] == selected_row or  new_col - col == selected_row - solution[col] or new_col - col == solution[col] - selected_row):
            safe = False
    return safe


print_solution = find_solution(size_of_nursery)[0]
print(print_solution)


print("Solved!!! HAHAHAHAHAAH...")
