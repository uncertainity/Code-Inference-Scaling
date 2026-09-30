n,k,p=map(int,input().split())
pk=(p+1)**k
INF=10**18
Ans=[INF]*(pk)
Ans[0]=0

for _ in range(n):
    c,*A=map(int,input().split())
    for i in range(pk-1,-1,-1):
        if Ans[i]!=INF:
            ii=i
            b=0
            for j in range(k):
                b+=min(p,ii%(p+1)+A[j])*((p+1)**j)
                ii//=(p+1)
            Ans[b]=min(Ans[b],Ans[i]+c)
print(-1 if Ans[-1]==INF else Ans[-1])