import heapq
#dijkstra
def main():
  n = int(input())
  graph = [[] for _ in range(n+1)]
  
  for i in range(1, n):
    a, b, x = map(int, input().split())
    graph[i].append((a, i+1))
    graph[i].append((b, x))
    
  # print(graph)
  
  dist = [float("inf")] * (n+1)
  dist[1] = 0
  # print(dist)
  
  hq = []
  heapq.heappush(hq, (0, 1))
  
  while hq:
    d, v = heapq.heappop(hq)
    if d > dist[v]:
      continue
    for nd, nv in graph[v]:
      if d + nd < dist[nv]:
        dist[nv] = d + nd
        heapq.heappush(hq, (d+nd, nv))
        
  print(dist[n])
  
main()