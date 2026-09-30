from sortedcontainers import SortedList

N,M=map(int,input().split())
P=list(map(int,input().split()))
L=list(map(int,input().split()))
D=list(map(int,input().split()))
C=[(L[i],D[i]) for i in range(M)]
C.sort(key=lambda x:x[1],reverse=True)

sl=SortedList()
for p in P:
    sl.add(p)

ans=0
for L,D in C:
    idx=sl.bisect_left(L)
    if idx==len(sl):
        continue
    ans+=sl[idx]-D
    sl.pop(idx)

for n in sl:
    ans+=n
print(ans)