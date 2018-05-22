'''
Given an array arr[] of n elements, write a function to search a given element x in arr[].

Examples :

Input : arr[] = {10, 20, 80, 30, 60, 50,
                     110, 100, 130, 170}
          x = 110;
Output : 6
Element x is present at index 6

Input : arr[] = {10, 20, 80, 30, 60, 50,
                     110, 100, 130, 170}
           x = 175;
Output : -1
Element x is not present in arr[].
'''
class LinearSearch:

    def search(self, x, arr):
        for elem in arr:
            if x==elem:
                return True

        return False

def main():
    search = LinearSearch()
    print(search.search(3, [5, 6, 0, 1, 3, 2]))

if __name__ == "__main__":
    main()