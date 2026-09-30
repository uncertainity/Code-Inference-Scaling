n = int(input())

adj = [list(map(int, input().split())) for _ in range(n)]

for i in range(n):
    ans = []
    for j in range(n):
        if adj[i][j] == 1:
            ans.append(str(j + 1))   # vertices are 1-indexed
    print(" ".join(ans))