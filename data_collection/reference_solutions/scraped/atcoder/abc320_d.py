n,m=map(int,input().split())

Next=[[] for _ in range(n)]

for _ in range(m):
    a,b,x,y=map(int,input().split())
    Next[a-1].append((b-1,x,y))
    Next[b-1].append((a-1,-x,-y))
q=[0]
Ans=[0]*n
Ans[0]=(0,0)
while q:
    a=q.pop()
    for i,j,k in Next[a]:
        if Ans[i]==0:
            q.append(i)
            Ans[i]=(Ans[a][0]+j,Ans[a][1]+k)
for i in Ans:
    if i:
        print(*i)
    else:
        print("undecidable")
