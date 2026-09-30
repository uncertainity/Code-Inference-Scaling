M = int(input())
D = list(map(int, input().split()))
Y = sum(D)//2
for i in range(M):
  if D[i] <= Y:
    Y -= D[i]
  else:
    print(i+1, Y+1)
    exit()