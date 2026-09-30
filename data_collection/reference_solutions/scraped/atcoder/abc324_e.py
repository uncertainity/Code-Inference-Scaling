import bisect

n,t=input().split()
n=int(n)
S=[input() for _ in range(n)]
S_a=[]
S_b=[]

for i in S:
    j=0
    for k in i:
        if t[j]==k:
            j+=1
        if j==len(t):
            break
    S_a.append(j)
    j=len(t)-1
    for k in i[::-1]:
        if t[j]==k:
            j-=1
        if j==-1:
            break
    S_b.append(j+1)

S_b.sort()

ans=0
for i in S_a:
    ans+=bisect.bisect_right(S_b,i)

print(ans)

