N,M = map(int,input().split())

if N == 2:
  print(0)
else:
  discord = N * (N - 1) / 2
  undiscordlist = []
  for i in range(M):
    a = list(map(int,input().split()))
    for i in range(N-1):
      if a[i] < a[i+1]:
        undiscord = a[i] * 100 + a[i+1]
      else:
        undiscord = a[i+1] * 100 + a[i]
      undiscordlist.append(undiscord)
  undiscordlist = set(undiscordlist)
  print(int(discord - len(undiscordlist)))