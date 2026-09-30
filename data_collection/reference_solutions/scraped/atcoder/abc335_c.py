n,q=map(int,input().split())
grid=[]
for i in range(n,0,-1):
    grid.append([i,0])
cnt=0
for _ in range(q):
    k,l=input().split()
    k=int(k)
    if k==1:
        if l=="U":
            head=grid[-1].copy()
            head[1]+=1
            grid.append(head)
        elif l=="D":
            head=grid[-1].copy()
            head[1]-=1
            grid.append(head)
        elif l=="R":
            head=grid[-1].copy()
            head[0]+=1
            grid.append(head)
        elif l=="L":
            head=grid[-1].copy()
            head[0]-=1
            grid.append(head)
        cnt+=1

    else:
        l=int(l)
        print(*grid[n-l+cnt])

        
