from collections import defaultdict
import heapq
N = int(input())
ice = defaultdict(list)
for _ in range(N):
  F, S = map(int, input().split())
  heapq.heappush(ice[F], -S)

ans = 0
uniq = []
for x in ice:
  uniq.append(heapq.heappop(ice[x]))
  if ice[x]:
    ans = min(ans, uniq[-1] + heapq.heappop(ice[x])//2)
uniq.sort()
if len(uniq) > 1:
  ans = min(ans, uniq[0]+uniq[1])
print(-ans)
