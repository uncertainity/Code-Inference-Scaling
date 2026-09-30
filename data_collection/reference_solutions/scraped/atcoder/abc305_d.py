def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC305 D 671 2Q - Sleep Log 450点
# 高橋くんは睡眠記録をつけています。睡眠記録は奇数長の数列A=(A1(=0),A2,…,AN)で表され、
# 奇数番目は起床時刻を、偶数番目は就寝時刻を表しています。
# より厳密には、睡眠記録をつけている間に高橋くんは次のような睡眠をとりました。
# ・すべての1≤i≤2 N-1 を満たす整数iについて、
# 睡眠記録をつけ始めてからA_{2 i}分後ちょうどに寝て、A_{2 i+1}分後ちょうどに起きた。
# ・それ以外の時間に寝ることも起きることもなかった。
# 次のQ個の質問に答えてください。i番目の質問では、0≤li≤ri≤ANを満たす整数の組(li,ri)が与えられます。
# ・睡眠記録をつけ始めてからli分後ちょうどからri分後ちょうどまでのri-li分のうち、高橋くんが寝ていたのは何分間ですか？
# ・3≤N<2×10^5 ・Nは奇数
# ・0=A1<A2<⋯<AN≤10^9
# ・1≤Q≤2×10^5
from bisect import bisect_right
N = ip()
A = lmp()
sleep = [0] * N
for i in range(1, N):
  sleep[i] = sleep[i - 1]
  if i % 2 == 0:
    sleep[i] += A[i] - A[i-1]
def f(t):
  i = bisect_right(A, t) - 1
  res = sleep[i]
  if i % 2 == 1:
    res += t - A[i]
  return res
for _ in range(ip()):
  l, r = mp()
  print(f(r) - f(l))
