def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC320 E 1096 1Q - Somen Nagashi 475点
# そうめん流しのイベントにN人の人が集まりました。人は一列に並んでおり、先頭から順に1からNの番号がついています。
# そうめん流しでは次の出来事がM回起こります。
# ・時刻Tiに量Wiのそうめんを流す。列の先頭にいる人がその全てを得る（誰も列に並んでいない場合は、誰もそのそうめんを得ない）。その人はいったん列から外れ、時刻Ti+Siに列の元の位置に戻ってくる。
# 時刻Xに列に戻ってくる人は、時刻Xには列に並んでいるとみなします。
# M回の出来事が全て行われたあと、それぞれの人が合計でどれだけそうめんを得ることができたか答えてください。
# ・1 ≤ N ≤ 2×10^5
# ・1 ≤ M ≤ 2×10^5
# ・0 < T1 < … < TM ≤ 10^9
# ・1 ≤ Si ≤ 10^9
# ・1 ≤ Wi ≤ 10^9
from heapq import heappop, heappush
N, M = mp()
event = []
for _ in range(M):
  t, w, s = mp()
  event.append((t, w, s))
que = []
for i in range(N):
  heappush(que, i)
ans = [0] * N
wait = []
for t, w, s in event:
  while wait and wait[0][0] <= t:
    _, i = heappop(wait)
    heappush(que, i)
  if que:
    i = heappop(que)
    ans[i] += w
    heappush(wait, (t + s, i))
print(*ans, sep='\n')