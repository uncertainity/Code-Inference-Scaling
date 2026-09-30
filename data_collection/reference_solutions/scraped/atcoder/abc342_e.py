n, m = map(int, input().split())
TR = [list(map(int, input().split())) for _ in range(m)]
E = [[] for _ in range(n)]

for i in range(m):
    a, b = TR[i][4:]
    a, b = a - 1, b - 1
    E[b].append((a, i))
inf = float("inf")

lasts = [-inf] * n
fixed = [False] * n
from heapq import heappop, heappush
q = []
heappush(q, (-inf, n - 1))

while q:
    l_, x = heappop(q)
    if lasts[x] > -l_:
        continue
    lasts[x] = -l_
    fixed[x] = True
    for y, i in E[x]:
        l, d, k, c, _, _ = TR[i]
        # l + k' * d + c <= lasts[x]
        # max(k')
        if fixed[y]:
            continue
        if l + c > lasts[x]:
            continue
        max_k = k - 1
        if l + (k - 1) * d + c > lasts[x]:
            # l + k'd + c <= last[x]
            # k' <= (last[x] - c - l) / d
            max_k = (lasts[x] - c - l) // d
        last = l + max_k * d
        if lasts[y] < last:
            heappush(q, (-last, y))

for i in range(n - 1):
    ans = lasts[i] if lasts[i] != -inf else "Unreachable"
    print(ans)