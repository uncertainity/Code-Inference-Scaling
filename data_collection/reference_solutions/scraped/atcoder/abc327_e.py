INF = 10 ** 18
N = int(input())
P = list(map(int, input().split()))

# dp[i] := 現在までに見たコンテストのうちi個選んだ時の、レート計算式の分子の最大値（分母とレートは後でまとめて計算する）
dp = [-INF] * (N + 1)
dp[0] = 0
for p in P:
    nx = dp[:]
    for i in range(N):
        if dp[i] == -INF: # 到達不能な状態からは遷移できない
            continue
        nx[i + 1] = max(nx[i + 1], dp[i] * 0.9 + p) # これまでの寄与を0.9倍した後に今回の寄与をを足すことで、0.9倍を累積できる
    dp = nx

# レート計算式の分母をO(1)で求めるため、累積和をとる
acc = [0] * (N + 1)
w = 1
for k in range(1, N + 1):
    acc[k] = acc[k - 1] + w
    w *= 0.9

ans = -INF
for k in range(1, N + 1):
    ans = max(ans, dp[k] / acc[k] - 1200 / k ** 0.5) # レートを計算
print(ans)