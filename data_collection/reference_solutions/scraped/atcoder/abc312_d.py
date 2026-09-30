s=input()
n=len(s)

MOD=998244353

dp=[[0 for _ in range(n+1)] for _ in range(n+1)]

dp[0][0]=1

for i in range(n):
    for j in range(n):
        if s[i]=="(":
            dp[i+1][j+1]=(dp[i][j]+dp[i+1][j+1])%MOD
        elif s[i]==")":
            if j-1>=0:
                dp[i+1][j-1]=(dp[i][j]+dp[i+1][j-1])%MOD
        else:
            dp[i+1][j+1]=(dp[i][j]+dp[i+1][j+1])%MOD
            if j-1>=0:
                    dp[i+1][j-1]=(dp[i][j]+dp[i+1][j-1])%MOD

print(dp[-1][0])
