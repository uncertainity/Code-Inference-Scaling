N, D = map(int, input().split())
s = []
for _ in range(N):
    s.append(list(input()))
ans = 0
cnt = 0
for j in range(D):
    f = True
    for i in range(N):
        if s[i][j] == 'x':
            f = False
            break
    if f:
        cnt += 1
    else:
        ans = max(ans, cnt)
        cnt = 0
ans = max(ans, cnt)
print(ans)