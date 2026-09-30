import sys
sys.setrecursionlimit(10**7)


n,m=list(map(int,input().split()))
g=[]
for _ in range(n):
    g.append(list(input()))

vis=[[False for _ in range(m)] for _ in range(n)]
ans=[[False for _ in range(m)] for _ in range(n)]

def dfs(pi,pj):
    vis[pi][pj]=True
    ans[pi][pj]=True

    for i,j in ((1,0),(-1,0),(0,1),(0,-1)):
        ni=pi
        nj=pj
        while g[ni+i][nj+j]==".":
            ni+=i
            nj+=j
            ans[ni][nj]=True
        if vis[ni][nj]==False:
            dfs(ni,nj)

dfs(1,1)

anss=0

for i in range(n):
    for j in range(m):
        if ans[i][j]:
            anss+=1

print(anss)




