def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC309 D 621 2Q - Add One Edge 400点
from collections import deque
N1, N2, M = mp()
N = N1 + N2
edge = [[] for _ in range(N)]
for _ in range(M):
  a, b = mp()
  a -= 1
  b -= 1
  edge[a].append(b)
  edge[b].append(a)
INF = 10**10
def bfs(st):
  dist = [INF] * N
  que = deque()
  que.append(st)
  dist[st] = 0
  while que:
    v = que.popleft()
    for to in edge[v]:
      if dist[to] != INF:
        continue
      dist[to] = dist[v] + 1
      que.append(to)
  return dist
dist0 = bfs(0)
dist1 = bfs(N-1)
ans0 = ans1 = 0
for d in dist0:
  if d != INF:
    ans0 = max(ans0, d)
for d in dist1:
  if d != INF:
    ans1 = max(ans1, d)
print(ans0 + ans1 + 1)