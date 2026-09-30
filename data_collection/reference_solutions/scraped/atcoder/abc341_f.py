N,M = map(int,input().split())

connected = [[] for _ in range(N)]

for _ in range(M):
  u,v = map(int,input().split())
  u -= 1
  v -= 1
  connected[u].append(v)
  connected[v].append(u)

W = list(map(int,input().split()))
A = list(map(int,input().split()))

hq = [(w,i) for i,w in enumerate(W)]
hq.sort()

res = [0]*N

for w,v in hq:
  L = len(connected[v])
  dp = [-float("inf")]*w
  dp[0] = 0
  
  #print(connected[v])
  for u in connected[v]:
    if W[u] >= w:
      continue
    dp_ = [-float("inf")]*w
    for c in range(w):
      dp_[c] = max(dp_[c], dp[c])
      if c+W[u] < w:
        dp_[c+W[u]] = max(dp_[c+W[u]], dp[c]+res[u])
    dp = dp_
    #print(u,dp)
  
  res[v] = max(dp)+1
  #print(v,w,dp,res)

ans = 0
for i in range(N):
  ans += A[i]*res[i]

print(ans)
  
  
  
  
  


