MOD = 998244353
N = int(input())
A = list(map(int, input().split()))
D = 10
S = 1 << (D + 1)
MASK = S - 1
dp = [0] * S
dp[1] = 1
p = 1
for a in A:
  p = p * a % MOD
  ndp = [0] * S
  for s in range(S):
    for r in range(1, min(D, a) + 1):
      ns = (s | s << r) & MASK
      ndp[ns] = (ndp[ns] + dp[s]) % MOD
    if a > D:
      ndp[s] = (ndp[s] + dp[s] * (a - D) % MOD) % MOD
  dp = ndp  
ans = 0
for s in range(S):
  if s & 1 << D:
    ans = (ans + dp[s]) % MOD
ans = ans * pow(p, -1, MOD) % MOD
print(ans)
