import heapq
oo = float("inf")

n, a, b, c = map(int, input().split())
d = [[*map(int, input().split())] for _ in range(n)]

dis = [[oo] * n for _ in range(2)]

for k, start in enumerate([0, n-1]):
  dij = [(0, start)]

  while dij:
    t, cur = heapq.heappop(dij)

    if t >= dis[k][cur]:
      continue
    dis[k][cur] = t
  
    for suc in range(n):
      tt = dis[k][cur] + (d[cur][suc]*a, d[suc][cur]*b + c)[k]
      if tt < dis[k][suc]:
        heapq.heappush(dij, (tt, suc))

print(min(map(sum, zip(*dis))))
