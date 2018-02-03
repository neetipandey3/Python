#!/bin/python3

#import numpy

'''
 Usage:
 
 Input line 1: _no of test cases
        Input line 2: n = no of items, k = maximum possible weight
        Input line 3: weights of available items
    
'''

from sys import setrecursionlimit
limit = 1000000
setrecursionlimit(limit)


def unboundedKnapsack(k, arr):
    # Complete this function
    maxInstances = 2000
    maxWeight = 2000
    knapsack = [[0] * maxInstances for _ in range(maxWeight)]
    #knapsack = numpy.zeros((maxInstances, maxWeight), dtype = int)

    for i in range(1, len(arr)+1):
        for j in range(1, k+1):
            if j >= arr[i-1]:
                knapsack[i][j] = max(knapsack[i-1][j], knapsack[i][j-arr[i-1]] + arr[i-1])
            else:
                knapsack[i][j] = knapsack[i-1][j]
    return knapsack[len(arr)][k]



if __name__ == "__main__":
    result = []
    t = int(input().strip())

    for _ in range(0, t):
        n, k = input().strip().split(' ')
        n, k = [int(n), int(k)]
        arr = list(map(int, input().strip().split(' ')))
        result.append(unboundedKnapsack(k, arr))
    for each in result:
        print(each)

