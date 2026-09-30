n=int(input())
A=list(map(int,input().split()))
X=[0]*(n+1)
Y=[0]*(n+1)
ans=0
for i in range(n):
   ans+=i*Y[A[i]]-X[A[i]]
   X[A[i]]+=i+1
   Y[A[i]]+=1
for y in Y:
   ans-=y*(y-1)*(y-2)//6
print(ans)