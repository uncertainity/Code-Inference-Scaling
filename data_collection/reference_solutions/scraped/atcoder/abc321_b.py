
N, X = map(int, input().split())

A = list(map(int, input().split()))

for n in range(0, 101):
    B = A[:] + [n]
    B.sort()
    if sum(B[1:-1]) >= X:
        print(n)
        exit()


print(-1)