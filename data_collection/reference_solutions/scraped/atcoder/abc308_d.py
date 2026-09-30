import sys

sys.setrecursionlimit(10**7)

from collections import deque
# from functools import cmp_to_key
from collections import defaultdict
import bisect
# import math
# import itertools
# import heapq

# from itertools import groupby
# import math
# from atcoder.dsu import DSU
# from functools import cache
# from sortedcontainers import SortedSet, SortedList, SortedDict

# from atcoder.fenwicktree import FenwickTree
# import copy
# import heapq

dr = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
]


def input():
    return sys.stdin.readline().strip()


def imap():
    return map(int, input().split())


def ilist():
    return list(map(int, input().split()))


H, W = imap()

S = []

for i in range(H):
    S.append(list(input()))

dq = deque()

# x,y,t文字目
dq.append((0, 0, 0))

xst = list("snuke")
isok = False
re = defaultdict(bool)
while len(dq) > 0:
    x, y, t = dq.popleft()

    if xst[t % 5] == S[x][y] and x == H - 1 and y == W - 1:
        isok = True
        break

    for dx, dy in dr:
        nx, ny = x + dx, y + dy

        if not (0 <= nx <= H - 1 and 0 <= ny <= W - 1):
            continue
        if not xst[(t + 1) % 5] == S[nx][ny]:

            continue

        if re[(nx, ny)]:
            continue
        dq.append((nx, ny, t + 1))
        re[(nx, ny)] = True

if isok:
    print("Yes")
else:
    print("No")
