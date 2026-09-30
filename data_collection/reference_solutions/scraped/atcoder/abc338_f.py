INF = 10 ** 18
N, M = map(int, input().split())
G = [[INF] * N for _ in range(N)]
for _ in range(M):
    u, v, w = map(int, input().split())
    G[u - 1][v - 1] = w
for v in range(N):
    G[v][v] = 0

def warshall_floyd(G):
    n = len(G)
    dist = [row[:] for row in G]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

dist = warshall_floyd(G)
dp = [[INF] * N for _ in range(1 << N)] # dp[mask][v] := 訪れた頂点集合がmaskで、最後に訪れた頂点がvのときの最短距離
for start in range(N):
    dp[1 << start][start] = 0
for mask in range(1 << N):
    for now in range(N):
        if (mask >> now) & 1 == 0:
            continue
        if dp[mask][now] == INF: # この状態には到達できない
            continue
        for to in range(N):
            if dist[now][to] == INF:
                continue
            if (mask >> to) & 1 == 1:
                continue
            nmask = mask | (1 << to)
            dp[nmask][to] = min(dp[nmask][to], dp[mask][now] + dist[now][to])

ans = INF
for goal in range(N):
    ans = min(ans, dp[(1 << N) - 1][goal])
print(ans if ans != INF else "No")