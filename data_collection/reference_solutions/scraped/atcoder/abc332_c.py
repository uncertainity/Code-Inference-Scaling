N,M = map(int,input().split())
S = list(input())

ans = 0
cnt = 0
muji = 0
rogo = 0
for word in S:
    if word == '1':
        muji += 1
    elif word == '2':
        rogo += 1
    else:
        if muji > M:
            cnt += (muji-M)+rogo
        else:
            cnt += rogo
        ans = max(ans,cnt)
        cnt = 0
        muji = 0
        rogo = 0
if muji > M:
    cnt += (muji-M)+rogo
else:
    cnt += rogo
ans = max(ans,cnt)
print(ans)