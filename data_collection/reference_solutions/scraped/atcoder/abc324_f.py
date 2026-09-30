from __future__ import annotations

import sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, cmp_to_key
from heapq import heapify, heappop, heappush
from itertools import accumulate, combinations, groupby, permutations, product
from math import acos, asin, atan, ceil, comb, cos, factorial, floor, gcd, isqrt, lcm, log2, perm, pi, sin, tan

sys.setrecursionlimit(10**9)
debug = lambda *args: __import__("devtools").debug(*args)
getint = lambda: int(input())
getints = lambda: list(map(int, input().split()))

N, M = getints()
graph = [[] for i in range(N)]
for j in range(M):
    u, v, b, c = getints()
    graph[u - 1].append((v - 1, b, c))

base = 10**10
l, r = 0, 10**18
inf = 10**18
while r - l > 1:
    mid = (r + l) // 2
    dp = [-inf] * N
    dp[0] = 0
    for i in range(N):
        for j, b, c in graph[i]:
            dp[j] = max(dp[j], dp[i] + base * b - mid * c)

    if dp[-1] >= 0:
        l = mid
    else:
        r = mid

print(l / base)
