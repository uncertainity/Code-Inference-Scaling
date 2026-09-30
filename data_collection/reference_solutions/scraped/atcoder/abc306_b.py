A = list(map(int, input().split()))
count = 0
for i in range(64):
  count += A[i] * (2 ** i)
  
print(count)