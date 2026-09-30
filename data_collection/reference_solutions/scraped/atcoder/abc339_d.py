from collections import deque
import sys
n=int(input())


p1=[-1,-1]
p2=[-1,-1]
grid=[["" for _ in range(n+2)] for _ in range(n+2)]
for i in range(n+2):
    grid[0][i]="#"
    grid[-1][i]="#"
    grid[i][0]="#"
    grid[i][-1]="#"

for i in range(n):
    s=input()
    for j in range(n):
        if s[j]=="P":
            if p1[0]==-1:
                p1=(i+1,j+1)
            else:
                p2=(i+1,j+1)
        grid[i+1][j+1]=s[j]

#for i in range(n+2):
 #   print(*grid[i])


dy=[-1,1,0,0]
dx=[0,0,-1,1]
vis=set([(p1,p2)])
v=deque([(p1,p2,0)])

while v:
    p1,p2,dep=v.popleft()
    if p1==p2:
        print(dep)
        sys.exit()
    y1,x1=p1
    y2,x2=p2

    for d in range(4):
        ny1,nx1,ny2,nx2=y1,x1,y2,x2
        ny1+=dy[d]
        nx1+=dx[d]
        ny2+=dy[d]
        nx2+=dx[d]
        if grid[ny1][nx1]=="#":
            ny1=y1
            nx1=x1
        if grid[ny2][nx2]=="#":
            ny2=y2
            nx2=x2
        if ((ny1,nx1),(ny2,nx2)) not in vis:
            vis.add(((ny1,nx1),(ny2,nx2)))
            v.append(((ny1,nx1),(ny2,nx2),dep+1))
print(-1)