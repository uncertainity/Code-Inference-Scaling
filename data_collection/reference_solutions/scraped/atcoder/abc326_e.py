N = int(input())
A = [0] + list(map(int, input().split()))
MOD = 998244353
invN = pow(N, MOD - 2, MOD)

dp = [0] * (N + 1) # dp[x]: 現在の変数がxの時の、これから得られる総額の期待値
acc = 0
for x in reversed(range(N)):
    acc = (acc + A[x + 1] + dp[x + 1]) % MOD # 現在の変数がxの時、遷移先それぞれについて「今後得る金額＋その後の期待値」の総和
    dp[x] = acc * invN % MOD # 期待値を計算（各遷移先は確率 1/N で選ばれる）

print(dp[0])