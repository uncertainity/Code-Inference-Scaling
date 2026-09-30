N = int(input())

for i in range(3, 10):
  if N <= (10**i - 1):
    N_str = str(N)
    length = len(N_str) - 3
    N_new = N_str[0:3] + "0"*length

print(N_new)
    
    