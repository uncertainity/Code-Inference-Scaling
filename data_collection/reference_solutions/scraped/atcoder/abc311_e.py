H, W, N = map(int, input().split())
holes = set(tuple(map(int, input().split())) for _ in range(N))

dp = [[0] * (W + 1) for _ in range(H + 1)] # dp[i][j] := マス(i,j)を右下とする、穴のない正方形の最大の一辺の長さ
ans = 0

for i in range(1, H + 1):
    for j in range(1, W + 1):
        # マスが穴なら飛ばす
        if (i, j) in holes:
            continue
        
        # マス(i,j)を右下とする、一辺の長さが k の正方形を作るには、
        # このマスの上・左・左上のマスを右下とする正方形の一辺の長さがそれぞれ少なくとも k-1 である必要があるので、
        # 作れる最大の一辺の長さは min(上,左,左上)+1
        dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
        
        ans += dp[i][j]

print(ans)