'''
Given a positive integer n, break it into the sum of at least two positive integers and maximize the product of those integers. Return the maximum product you can get.

For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).
'''
class IntegerBreak:
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """
def main():
    search = IntegerBreak()
    print(search.search(3, [5, 6, 0, 1, 3, 2]))

if __name__ == "__main__":
    main()