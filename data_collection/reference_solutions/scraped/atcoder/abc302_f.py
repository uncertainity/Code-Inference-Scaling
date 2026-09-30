from collections import deque

def solve():
  n, m = map(int, input().split())
  a = [[] for _ in range(m)] # set index -> values(0, m - 1)
  b = [[] for _ in range(n)] # values(0, m - 1) -> set index

  for i in range(n):
    sz = int(input())
    b[i] = [int(_) - 1 for _ in input().split()]
    for j in b[i]:
      a[j].append(i)
  
  qu = deque(a[0]) # set index
  vis = [0] * n # set
  vis1 = [0] * m # values
  ans = 0

  for u in a[0]:
    vis[u] = 1

  while len(qu) > 0:
    sz = len(qu)
    while sz > 0 :
      u = qu.popleft()
      for x in b[u]:
        if x == m - 1:
          print(ans)
          return
        if vis1[x] == 1:
          continue
        vis1[x] = 1
        for v in a[x]:
          if vis[v] == 1:
            continue
          qu.append(v)
          vis[v] = 1        
      sz -= 1
    ans += 1
  
  print(-1)

  pass

if __name__ == '__main__':
  solve()