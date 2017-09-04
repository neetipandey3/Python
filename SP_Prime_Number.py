
print("Input: ")
no_of_test_case = int(input())

prime_numbers = ""
prime = True

#Looping for total number of test cases from input
while no_of_test_case > 0:
    prime_range = input().split(" ")  #Neeti: need to take input in the beginning and break it off (later)
    #prime_numbers = [str]
    range_begins = int(prime_range[0])
    range_ends = int(prime_range[1])

#Initializing the range for all even numbers and 1
    if(range_begins in (1,2)):
        prime_numbers += "\n2"
        range_begins = 3
    elif(range_begins%2 == 0):
        range_begins += 1

#Checking every odd number to be a prime; skipping all the even numbers (num+=2)
    num = range_begins
    while(num <= range_ends):
        for div in range(2,num):
            if (num%div == 0):
                prime = False
                break
        if prime:
                prime_numbers += "\n{}".format(num)

        num += 2
        prime = True

    prime_numbers += "\n\n"
    no_of_test_case -= 1

print("\nOutput : {}".format(prime_numbers))

print("Whoa!!!!...Success :)")
