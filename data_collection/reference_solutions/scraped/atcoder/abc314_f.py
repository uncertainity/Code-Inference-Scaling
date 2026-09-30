from atcoder.dsu import DSU
from collections import deque
mod=998244353

n=int(input())
m=2*n-1

uf=DSU(n)
node=list(range(m))

graph=[[] for _ in range(m)]
for i in range(n,m):
    p,q=map(lambda x:int(x)-1,input().split())
    lp=uf.leader(p)
    lq=uf.leader(q)

    node_p=node[lp]
    node_q=node[lq]

    sp=uf.size(lp)
    sq=uf.size(lq)
    inv=pow(sp+sq,mod-2,mod)

    graph[i].append((node_p,sp*inv%mod))
    graph[i].append((node_q,sq*inv%mod))

    node[uf.merge(p,q)]=i

que=deque([(m-1,0)])
ans=[0]*n

while que:
    u,p=que.popleft()
    if u<n:
        ans[u]=p
        continue
    
    for v,next_p in graph[u]:
        que.append((v,(p+next_p)%mod))

print(*ans)
