import time
import random
import math
import collections
import copy

start_time = time.time()
input_file = open("./input.txt", "r", encoding="utf-8")
output_file = open("./output.txt", "w", encoding="utf-8")
board_size = int(input_file.readline())
no_fruits_types = input_file.readline()
time_left = input_file.readline()

input_matrix = []

for _ in range(board_size):
    input_matrix.append(list(input_file.readline().strip()))
    if(len(input_matrix[-1]) != board_size):
        output_file.write("FAIL")
        output_file.close()
        exit("FAIL")

board = copy.deepcopy(input_matrix)
state = input_matrix

for i in range (board_size):
    print(input_matrix[i], sep = "")

neighbours_dict = {}
start_starts_at_dict = {}
def find_next_neighbours(state):
    for col in range(board_size):
        for row in range(board_size-1, -1, -1):
            selected_fruit = state[row][col]
            if selected_fruit == '*':
                start_starts_at_dict.update({col : row})
                break;
            neighbours = []
            if (row-1 >= 0 and state[row-1][col] == selected_fruit):
                neighbours.append((row-1, col))
            if (col-1 >= 0 and state[row][col-1] == selected_fruit):
                neighbours.append((row, col-1))
            if (row+1 < board_size and state[row+1][col] == selected_fruit):
                neighbours.append((row+1, col))
            if (col+1 < board_size and state[row][col+1] == selected_fruit):
                neighbours.append((row, col+1))
            neighbours_dict.update({(row, col): neighbours})
            #print("neighbours_dict {}".format(neighbours_dict))
    return neighbours_dict

def find_cluster(row, col):
    """find the cluster of same fruit type based on the selected position"""
    cluster = []
    tracker = []
    cluster.append((row, col))
    tracker.append((row, col))
    while(tracker):
        neighbours = neighbours_dict[tracker.pop()]
        for (r, c) in neighbours:
            if ((r, c) not in cluster):
                cluster.append((r, c))
                tracker.append((r, c))
                #print("cluster {}".format(cluster))
    return cluster

def get_next_state(cur_board, row, col):
    row_cut_off_dict = {}
    """ get the next board state by finding and then sliding the cluster """
    selected_cluster = find_cluster(row, col)
    for (r, c) in selected_cluster:
        cur_board[r][c] = '*'
        if(row_cut_off_dict.get(c)):
            row_cut_off_dict[c] = min(row_cut_off_dict[c], r)
        else:
            row_cut_off_dict.update({c : r})

    for column, lowest_row_to_slide_to in row_cut_off_dict.items():
        for row in range(lowest_row_to_slide_to, -1, -1):
            if(row-1 >= 0):
                cur_board[row][column] = cur_board[row-1][column]
                cur_board[row-1][column] = '*'
            if(row-2 >= 0 and cur_board[row-2][column] == '*'):
                continue
    print("")
    for i in range (board_size):
        print(cur_board[i], sep = "")
    return cur_board


best_set_of_moves = {}
def find_next_moves():
    """Find next set of available moves - excluding the stars on board
    Returns:
    1. Dictionary of best set of moves - KEY = MOVE; VALUE = CLUSTER_SIZE
    """
    next_moves = []
    columns_with_stars = start_starts_at_dict.keys()
    for col in range(board_size):
        for row in range(board_size-1, -1, -1):
            if(col in columns_with_stars and row == start_starts_at_dict.get(col)):
                break
            next_moves.append((row, col))

    while(next_moves):
        row, col = next_moves.pop()
        cluster = find_cluster(row, col)
        best_set_of_moves.update({(row, col): len(cluster)})
        next_moves = set(next_moves) - set(cluster)

    print("best_set_of_moves {}".format(best_set_of_moves))
    return best_set_of_moves


score_MAX = []
score_MIN = []
def alpha_beta_minmax(next_state, depth, alpha=float("-inf"), beta=float("inf"), MAX=True):
    """Find the best move using minimax-alpha-beta-pruning
    Returns:
    1. maximum score
    2. best move """
        #if time_left() < TIMER_THRESHOLD:
        #    raise Timeout()
    find_next_neighbours(next_state)
    next_moves = find_next_moves()
    if (not next_moves) or (depth == 0):
        if MAX:
            return (get_score(MAX), (-1, -1))
        else:
            return (get_score(not MAX), (-1, -1))

    if MAX:
        max_score = float("-inf")
        for (move_row, move_col), value in next_moves.copy().items():
            next_state = get_next_state(state, move_row, move_col)
            child_score, child_move = alpha_beta_minmax(next_state, depth-1, alpha, beta, not MAX)

            if child_score >= max_score:
                max_score, (selected_row, selected_col) = child_score, (move_row, move_col)
            """ If the branch utility is greater than beta, prune other sibling branches. """
            if max_score >= beta:
                return max_score, (selected_row, selected_col)
            """ If branch utility is greater than current score of alpha for MAX nodes, update alpha """
            alpha = max(alpha, max_score)
            score_MAX.append(next_moves.get((move_row, move_col)))
        return max_score, (selected_row, selected_col)

    else:
        min_score = float("inf")
        for (move_row, move_col), value in next_moves.copy().items():
            next_state = get_next_state(state, move_row, move_col)
            child_score, child_move = alpha_beta_minmax(next_state, depth-1, alpha, beta, MAX)
            if child_score <= min_score:
                min_score, (selected_row, selected_col) = child_score, (move_row, move_col)
            """ If the branch utility is less than alpha, prune other sibling branches."""
            if min_score <= alpha:
                return min_score, (selected_row, selected_col)
            """ If branch utility is lesser than current score of beta for MIN nodes, update beta """
            beta = min(beta, min_score)
            score_MIN.append(next_moves.get((move_row, move_col)))
    return min_score, (selected_row, selected_col)


def get_score(MAX):
    score = float("-inf")
    print("score_MAX {}".format(score_MAX))
    print("score_MIN {}".format(score_MIN))
    while(score_MAX):
        score += score_MAX.pop()**2
    while(score_MIN):
        score -= score_MIN.pop()**2
    return score

score, (row, col) = alpha_beta_minmax(state, depth = 10, alpha=float("-inf"), beta=float("inf"), MAX=True)
print("Output {}  Row {} Col {}".format(score, row, col))

print("input {}".format(board))
find_next_neighbours(board)
print("Next_State {}".format(get_next_state(board, row, col)))
