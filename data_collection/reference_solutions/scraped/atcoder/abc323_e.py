MOD = 998244353
n, x = map(int, input().split())
t = list(map(int, input().split()))
invN = pow(n, -1, MOD)
dp0 = [0] * (x + 2)
dp1 = [0] * (x + 2)
dp0[min(x + 1, t[0])] += invN
for i in range(1, n):
    dp1[min(x + 1, t[i])] += invN
    dp1[min(x + 1, t[i])] %= MOD

for c in range(x + 1):
    base = (dp0[c] + dp1[c]) * invN
    base %= MOD
    dp0[min(x + 1, c + t[0])] += base
    dp0[min(x + 1, c + t[0])] %= MOD
    for i in range(1, n):
        dp1[min(x + 1, c + t[i])] += base
        dp1[min(x + 1, c + t[i])] %= MOD
print(dp0[x + 1])
