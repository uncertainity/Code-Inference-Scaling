import sys 
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

N,M=map(int,input().split())
X=list(map(int,input().split()))
ans=[0]*(N+2) #ans[i]でiへ右回りで来る箸
last=X[0]
for x in X[1:]:
    tmp=x
    val1=abs(x-last)
    val2=N-val1
    last,x=min(last,x),max(last,x)
    ans[last+1]+=val2
    ans[x+1]-=val2
    ans[1]+=val1
    ans[last+1]-=val1
    ans[x+1]+=val1
    ans[N+1]-=val1
    last=tmp

def prefix_sum(A):
    S=[0]*(len(A)+1)
    for i in range(len(A)):
        S[i+1]=S[i]+A[i]
    return S

ans=prefix_sum(ans)[2:N+2]
print(min(ans))