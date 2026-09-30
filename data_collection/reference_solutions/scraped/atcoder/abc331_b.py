n, s, m, l = map(int,input().split())
ans = 10**6 + 1

for i in range(101):
    for j in range(101):
        for k in range(101):
            if i*6 + j*8 + k*12 >= n:
                ans = min(ans, i*s + j*m + k*l)

print(ans)