import sys
sys.setrecursionlimit(10 ** 6)

N, M = map(int, input().split())
G = [[] for _ in range(N + 1)]
for c, p in enumerate(map(int, input().split()), start=2):
    G[p].append(c)

remain = [-1] * (N + 1) # remain[v] := 頂点vで有効な保険の残りの深さ
for _ in range(M):
    x, y = map(int, input().split())
    remain[x] = max(remain[x], y)

def dfs(now, depth):
    remain[now] = max(remain[now], depth)
    for to in G[now]:
        dfs(to, remain[now] - 1)

dfs(1, remain[1])
ans = sum(1 for v in range(1, N + 1) if remain[v] >= 0)
print(ans)