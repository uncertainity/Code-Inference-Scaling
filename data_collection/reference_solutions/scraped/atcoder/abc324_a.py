N = input()
numbers = list(map(int, input().split()))

ref = numbers[0]
all_equal = True

for i in numbers:
  if i != ref:
    all_equal = False
    break
    
if all_equal:
  print("Yes")
else:
  print("No")
  
