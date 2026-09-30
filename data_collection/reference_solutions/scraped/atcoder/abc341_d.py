def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC341 D 829 2Q - Only one of two 400点
# 正整数 N, M, K が与えられます。
# ここで、N と M は異なります。
# 正の整数であって、N と M のうち ちょうど一方のみ で割り切れる数のうち
# 小さい方から K 番目のものを出力してください。
# ・1 ≤ N,M ≤ 10^8
# ・1 ≤ K ≤ 10^10
from math import lcm
N, M, K = mp()
L = lcm(N, M)
def judge(x):
  return x // N + x // M - 2 * (x // L) >= K
ng, ok = 0, 10**18
while ok - ng > 1:
  mi = (ng + ok) // 2
  if judge(mi):
    ok = mi
  else:
    ng = mi
print(ok)