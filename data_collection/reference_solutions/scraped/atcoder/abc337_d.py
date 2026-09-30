import sys 
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

ans=10**17
H,W,K=map(int,input().split())
grid=[input().strip() for _ in range(H)]
for g in grid:
    gg=g.split("x")
    for s in gg:
        s=list(s)
        n=len(s)

        dot = 0
        ans2 = 10**18
        r = 0

        for l in range(n):
            while r < n and r - l < K:
                if s[r] == ".":
                    dot += 1
                r += 1

            if r - l >= K:
                ans2 = min(ans2, dot)

            if s[l] == ".":
                dot -= 1
        ans=min(ans,ans2)
grid=[list(g) for g in grid]
next=[["" for _ in range(H)] for _ in range(W)]
for i in range(H):
    for j in range(W):
        next[j][i]=grid[i][j]
for g in next:
    g="".join(g)
    gg=g.split("x")
    for s in gg:
        s=list(s)
        n=len(s)

        dot = 0
        ans2 = 10**18
        r = 0

        for l in range(n):
            while r < n and r - l < K:
                if s[r] == ".":
                    dot += 1
                r += 1

            if r - l >= K:
                ans2 = min(ans2, dot)

            if s[l] == ".":
                dot -= 1
        ans=min(ans,ans2)
if ans>=10**16:
    print(-1)
else:
    print(ans)