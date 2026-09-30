import bisect
a=[i**2 for i in range(2*10**6)]

d=int(input())



ans=10**18
for i in a:
    ans=min(ans,abs(i+a[bisect.bisect_left(a,d-i)]-d))
    ans=min(ans,abs(i+a[bisect.bisect_left(a,d-i)-1]-d))
print(ans)