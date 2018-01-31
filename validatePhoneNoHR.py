import re

no_of_inputs = int(input())
if no_of_inputs < 1 or no_of_inputs >10:
    print("Invalid no of inputs")

for _ in range(0, no_of_inputs):
    phone_no = input()
    if len(phone_no) < 10 or len(phone_no) > 10:
        print("NO")
        continue
    match = re.match(r'[789]{1}\d{9}', phone_no)
    if not match:
        print("NO")
        continue
    else:
        print("YES")
        continue


