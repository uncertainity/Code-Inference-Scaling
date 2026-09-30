N = int(input())
L = [[0] * 103 for _ in range(103)]

for _ in range(N):
    r1, r2, c1, c2 = map(int, input().split())
    r1 += 1; r2 += 1; c1 += 1; c2 += 1
    L[r1][c1] += 1
    L[r1][c2] -= 1
    L[r2][c1] -= 1
    L[r2][c2] += 1

for i in range(1, 102):
    for j in range(1, 102):
        L[i][j] += L[i][j - 1]

for j in range(1, 102):
    for i in range(1, 102):
        L[i][j] += L[i - 1][j]

ans = 0
for LL in L:
    for i in LL:
        if i > 0 :
            ans += 1

print(ans)