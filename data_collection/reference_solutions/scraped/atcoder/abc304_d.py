w,h=list(map(int,input().split()))
n=int(input())
itigo=[]
for _ in range(n):
    p,q=list(map(int,input().split()))
    itigo.append((p,q))
a=int(input())
aa=[0]+list(map(int,input().split()))+[w]
b=int(input())
bb=[0]+list(map(int,input().split()))+[h]

import collections
ans=collections.defaultdict(int)

import bisect

for p,q in itigo:
    i=bisect.bisect_left(aa,p)
    j=bisect.bisect_left(bb,q)
    ans[(i,j)]+=1

maxx=0
minn=10**20
c=0

for x,y in ans.items():
    c+=1
    maxx=max(maxx,y)
    minn=min(minn,y)

if c!=(a+1)*(b+1):
    minn=0

print(minn,maxx)