
S = input().strip()
N = int(input())
L = len(S)

ans = 0


for i, ch in enumerate(S):
    if ch == '1':
        bit = L - 1 - i
        ans += 1 << bit

if ans > N:
    print(-1)
    exit()
    
for i, ch in enumerate(S):
    if ch == '?':
        bit = L - 1 - i
        add = 1 << bit

        if ans + add <= N:
            ans += add

print(ans)