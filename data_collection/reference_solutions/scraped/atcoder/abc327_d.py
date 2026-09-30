import sys
sys.setrecursionlimit(10 ** 9)

def dfs(x):
    global result
    if seen[x] == -1:
        seen[x] = 0
    for dx in g[x]:
        if seen[x] == seen[dx]:
            result = False
        elif seen[dx] == -1:
            if seen[x] == 0:
                seen[dx] = 1
            else:
                seen[dx] = 0
            dfs(dx)

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

g = [[] for _ in range(n)]
for i in range(m):
    g[a[i]-1].append(b[i]-1)
    g[b[i]-1].append(a[i]-1)
seen = [-1] * n
result = True
for i in range(n):
    dfs(i)
print("Yes" if result else "No")