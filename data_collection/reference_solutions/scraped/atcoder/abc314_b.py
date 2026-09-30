N = int(input())
ans = []
L = [(38, []) for _ in range(37)]
for i in range(1, N + 1):
    C = int(input())
    A = list(map(int, input().split()))
    for a in A:
        if L[a][0] > C:
            L[a] = (C, [i])
        elif L[a][0] == C:
            L[a][1].append(i)

X = int(input())
print(len(L[X][1]))
print(*L[X][1])