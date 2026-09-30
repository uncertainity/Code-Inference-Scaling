N,Q = map(int,input().split())
S = str(input())
num = 0
ans = [0]*N
if N != 1:
    for i in range(1,N):
        if S[i] == S[i-1]:
            num += 1
        ans[i] = num

for _ in range(Q):
    l,r = map(int,input().split())
    if N == 1:
        print(0)
    else:
        print(ans[r-1]-ans[l-1])