
n,m=map(int,input().split())
a=list(map(int,input().split()))
ans=[0]*(n+1)
j=0
for i in range(1,n+1):
 if a[j]>i:
  ans[i]=a[j]-i
 else:
  j+=1
  ans[i]=0

print("\n".join(map(str,ans[1:])))