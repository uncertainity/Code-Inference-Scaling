def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC312 C 727 2Q - Invisible Hand 300点
N, M = mp()
A = lmp()
B = lmp()
def judge(x):
  acnt, bcnt = 0, 0
  for a in A:
    if a <= x:
      acnt += 1
  for b in B:
    if b >= x:
      bcnt += 1
  return acnt >= bcnt
ng, ok = 0, 10**10
while ok - ng > 1:
  mi = (ok + ng) // 2
  if judge(mi):
    ok = mi
  else:
    ng = mi
print(ok)