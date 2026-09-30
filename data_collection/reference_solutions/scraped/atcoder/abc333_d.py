def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC333 D 704 2Q - Erase Leaves 400点
# 頂点 1, 頂点 2,…, 頂点 N の N 個の頂点からなる木が与えられます。 
# i 番目 (1≤i<N) の辺は頂点 ui と vi を結んでいます。
# 次の操作を好きな回数繰り返すことを考えます。
# 葉である頂点 v を 1 つ選び、頂点 v およびそれに接続する辺をすべて削除する。
# 頂点 1 を削除するまでに最小で操作を何回行う必要があるか求めてください。
# ・2 ≤ N ≤ 3×10^5
from atcoder.dsu import DSU
N = ip()
uf = DSU(N)
for _ in range(N-1):
  u, v = mp()
  u -= 1
  v -= 1
  if u == 0 or v == 0:
    continue
  uf.merge(u, v)
ans = N - max(uf.size(v) for v in range(N))
print(ans)
