N = int(input())
P = list(map(int, input().split()))
pos = [0] * (N + 1)
for i in range(N):
    pos[P[i]] = i
Q = int(input())
for _ in range(Q):
    A, B = map(int, input().split())
    if pos[A] < pos[B]:
        print(A)
    else:
        print(B)
