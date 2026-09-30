def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC334 D 602 3Q - Reindeer and Sleigh 400点
# N 台のソリがあり、各ソリには 1,2,…,N の番号がつけられています。
# ソリ i を引くために必要なトナカイは Ri 匹です。
# また、各トナカイが引けるソリは高々 1 台です。
# より厳密には、m 台のソリ i1,i2,…,im を引くために必要なトナカイは ∑_{k=1}^m Rik 匹です。
# 以下の形式のクエリが Q 個与えられるので、答えを求めてください。
# 整数 X が与えられる。トナカイが X 匹いるときに最大で何台のソリを引けるか求めよ。
# ・1 ≤ N,Q ≤ 2×10^5
# ・1 ≤ Ri ≤ 10^9
# ・1 ≤ X ≤ 2×10^14
from bisect import bisect_right
N, Q = mp()
R = lmp()
R.sort()
cum = [0] * (N+1)
for i in range(N):
  cum[i+1] = cum[i] + R[i]
for _ in range(Q):
  X = ip()
  i = bisect_right(cum, X)
  print(i-1)
