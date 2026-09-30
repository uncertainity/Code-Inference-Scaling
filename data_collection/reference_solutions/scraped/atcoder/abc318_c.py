import sys
def input():return sys.stdin.readline().strip()
def rev(x,y):return range(y-1,x-1,-1)

n,d,p = map(int,input().split())
f = list(map(int,input().split()))
f.sort()
ans = 0
cnt = 0
cntsum = 0
for i in rev(0,n):
    ans += f[i]
    cntsum += f[i]
    cnt += 1
    if cnt==d:
        if cntsum>p:
            ans -= cntsum
            ans += p
        cnt = 0
        cntsum = 0
if cntsum>p:
    ans -= cntsum
    ans += p
print(ans)