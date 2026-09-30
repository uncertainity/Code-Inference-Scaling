MOD = 998244353

def code(s):
    return ord(s)-ord("A")
def code2(s):
    return ord(s)-ord("a")
def codeR(n):
    return chr(ord("A")+n)

S = input()[::-1]
N = len(S)

nex = [[0]*26 for _ in range(N+1)]
for i in reversed(range(N)):
    for j in range(26):
        nex[i][j] = nex[i+1][j]
    if S[i].isupper():
        nex[i][code(S[i])] += 1

dp = [[0]*29 for _ in range(N+1)]
dp[0][0] = 1
for i in range(N):
    cnt = 0
    flag = False
    for j in range(26):
        if nex[i+1][j] == 1:
            cnt += 1
        elif 2 <= nex[i+1][j]:
            flag = True
    for j in range(29):
        if dp[i][j] == 0:
            continue
        if j == 0:
            for k in range(26):
                if S[i] == "?" or S[i].isupper() and code(S[i]) == k:
                    dp[i+1][j+1] += dp[i][j]
                    dp[i+1][j+1] %= MOD
            for k in range(26):
                if S[i] == "?" or S[i].islower() and code2(S[i]) == k:
                    dp[i+1][j] += dp[i][j]
                    dp[i+1][j] %= MOD
        elif j == 1:
            for k in range(26):
                if S[i] == "?" or S[i].isupper() and code(S[i]) == k:
                    dp[i+1][j] += dp[i][j]
                    dp[i+1][j] %= MOD
            for k in range(26):
                if (S[i] == "?" or S[i].islower() and code2(S[i]) == k) and not flag:
                    dp[i+1][j+1+cnt] += dp[i][j]
                    dp[i+1][j+1+cnt] %= MOD
        else:
            if S[i] == "?":
                dp[i+1][j] += dp[i][j]*26%MOD
                dp[i+1][j] %= MOD
                if j+1 < 29:
                    dp[i+1][j+1] += dp[i][j]*(28-j)%MOD
                    dp[i+1][j+1] %= MOD
            else:
                dp[i+1][j] += dp[i][j]
                dp[i+1][j] %= MOD

print(sum(dp[-1])%MOD)