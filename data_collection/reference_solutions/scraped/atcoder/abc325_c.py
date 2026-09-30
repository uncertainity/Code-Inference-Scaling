import sys
sys.setrecursionlimit(10 ** 9)

def dfs(di, dj):
    for move in range(8):
        mi = di + move_i[move]
        mj = dj + move_j[move]
        if 0 <= mi < h and 0 <= mj < w and s[mi][mj] == "#" and not seen[mi][mj]:
            seen[mi][mj] = True
            dfs(mi, mj)

h, w = map(int, input().split())
s = [input() for _ in range(h)]

seen = [[False for _ in range(w)] for _ in range(h)]
move_i = [-1, -1, 0, 1, 1, 1, 0, -1]
move_j = [0, 1, 1, 1, 0, -1, -1, -1]

ans = 0
for i in range(h):
    for j in range(w):
        if s[i][j] == "#" and not seen[i][j]:
            ans += 1
            dfs(i, j)

print(ans)

