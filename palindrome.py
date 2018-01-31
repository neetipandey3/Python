

stack = []
queue = []
class Solution:

    def pushCharacter(self, string_char):
        stack.append(string_char)

    def enqueueCharacter(self, string_char):
        queue.append(string_char)

    def popCharacter(self):
        return stack.pop()

    def dequeueCharacter(self):
        queue.reverse()
        q_pop = queue.pop()
        queue.reverse()
        return q_pop



# read the string s
s = input()
# Create the Solution class object
obj = Solution()

l = len(s)
# push/enqueue all the characters of string s to stack
for i in range(l):
    obj.pushCharacter(s[i])
    obj.enqueueCharacter(s[i])

isPalindrome = True
'''
pop the top character from stack
dequeue the first character from queue
compare both the characters
'''
for i in range(l // 2):
    a = obj.popCharacter()
    b = obj.dequeueCharacter()
    print("a = ", a)
    print("b = ", b)
    if a != b:
        isPalindrome = False
        break
# finally print whether string s is palindrome or not.
if isPalindrome:
    print("The word, " + s + ", is a palindrome.")
else:
    print("The word, " + s + ", is not a palindrome.")