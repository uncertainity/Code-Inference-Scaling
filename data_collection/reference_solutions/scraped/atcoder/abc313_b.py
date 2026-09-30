N, M = map(int, input().split())
b = set()

for _ in range(M):
    A, B = map(int, input().split())
    b.add(B)

S = set(range(1, N + 1))
if len(S - b) == 1:
    print(*(S - b))
else:
    print(-1)