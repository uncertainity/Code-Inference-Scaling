from collections import deque

INF = 10 ** 18
H, W, T = map(int, input().split())
A = [input() for _ in range(H)]

ID = 0 # 各お菓子マスの頂点番号
vertex = {} # お菓子マス、スタート地点、ゴール地点の頂点番号を記録
for i in range(H):
    for j in range(W):
        match A[i][j]:
            case "S":
                si, sj = i, j
            case "G":
                gi, gj = i, j
            case "o":
                vertex[(i, j)] = ID
                ID += 1

start = ID # スタート地点の頂点番号をID、ゴール地点の頂点番号をID+1とする
goal = ID + 1
vertex[(si, sj)] = start
vertex[(gi, gj)] = goal

def bfs(i, j):
    startID = vertex[(i, j)]
    dist = [[INF] * W for _ in range(H)]
    dist[i][j] = 0
    que = deque()
    que.append((i, j))
    while que:
        i, j = que.popleft()
        if (i, j) in vertex:
            goalID = vertex[(i, j)]
            dist_matrix[startID][goalID] = dist[i][j]
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            ni, nj = i + di, j + dj
            if not (0 <= ni < H and 0 <= nj < W):
                continue
            if A[ni][nj] == "#":
                continue
            if dist[ni][nj] != INF:
                continue
            dist[ni][nj] = dist[i][j] + 1
            que.append((ni, nj))

dist_matrix = [[INF] * (ID + 2) for _ in range(ID + 2)] # スタート地点、ゴール地点、各お菓子マスの全頂点対間距離の行列
for i, j in vertex.keys():
    bfs(i, j)

# dist[mask][v] := スタート地点から開始し、訪れたお菓子マスの集合がmaskであり、最後にお菓子マスvにいる時の、最小移動回数
dp = [[INF] * ID for _ in range(1 << ID)]
for v in range(ID):
    dp[1 << v][v] = dist_matrix[start][v]

for mask in range(1 << ID):
    for now in range(ID):
        if (mask >> now) & 1 == 0: # 頂点nowに未訪問の場合
            continue
        if dp[mask][now] == INF: # この状態に到達不可の場合
            continue
        for to in range(ID):
            if (mask >> to) & 1 == 1: # 頂点toに既に到達済みの場合
                continue
            if dist_matrix[now][to] == INF: # 頂点nowからtoへ到達不可の場合
                continue
            nmask = mask | (1 << to)
            dp[nmask][to] = min(dp[nmask][to], dp[mask][now] + dist_matrix[now][to])

ans = -1
if dist_matrix[start][goal] <= T: # お菓子マスが無い場合
    ans = 0
for mask in range(1 << ID):
    for v in range(ID):
        if dp[mask][v] == INF:
            continue
        if dist_matrix[v][goal] == INF:
            continue
        if dp[mask][v] + dist_matrix[v][goal] > T:
            continue
        ans = max(ans, mask.bit_count())
print(ans)