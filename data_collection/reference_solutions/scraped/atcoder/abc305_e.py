def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC305 E 1158 1Q - Art Gallery on Graph 475点
# # 頂点に 1 から N の、辺に 1 から M の番号がついた N 頂点 M 辺の単純無向グラフがあります。
# 辺 i は頂点 ai と頂点 bi を結んでいます。
# 1 から K までの番号がついた K 人の警備員が頂点上にいます。
# 警備員 i は頂点 pi にいて、体力は hi です。
# ここで全ての pi は互いに異なります。
# 頂点 v が次の条件を満たす時、頂点 v を 警備されている頂点 と呼びます。
# ・頂点 v と頂点 pi の距離が hi 以下であるような警備員 i が少なくとも 1 人存在する。
# ここで、頂点 u と頂点 v の距離とは、頂点 u と頂点 v を結ぶパスに含まれる辺の本数の最小値のことをいいます。
# グラフに含まれる頂点のうち、警備されている頂点を 小さい方から順に 全て列挙してください。
# ・1 ≤ N ≤ 2×10^5
from heapq import heappop, heappush
N, M, K = mp()
edge = [[] for _ in range(N)]
for _ in range(M):
  a, b = mp()
  a -= 1
  b -= 1
  edge[a].append(b)
  edge[b].append(a)
que = []
pow = [-1] * N
for _ in range(K):
  p, h = mp()
  p -= 1
  heappush(que, (-h, p))
  pow[p] = h
while que:
  h, p = heappop(que)
  h = -h
  if pow[p] > h:
    continue
  for to in edge[p]:
    # if pow[to] != -1:
    #   continue
    if pow[to] < h - 1:
      pow[to] = h - 1
      heappush(que, (-h+1, to))
ans = []
for i in range(N):
  if pow[i] >= 0:
    ans.append(i+1)
print(len(ans))
print(*ans)