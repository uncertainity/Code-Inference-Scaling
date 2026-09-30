from collections import deque, defaultdict, Counter
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations, groupby
from heapq import heappop, heappush
import math, sys
input = lambda: sys.stdin.readline().rstrip("\r\n")
def printl(li, sep=" "): print(sep.join(map(str, li)))
def yn(flag): print(Yes if flag else No)
_int = lambda x: int(x)-1
MOD = 998244353 #10**9+7
INF = 1<<60
Yes, No = "Yes", "No"

N = int(input())
S = input()
memo = [0]*10
for c in S: memo[int(c)] += 1

M = 4000000
ans = 0
for n in range(M):
    num = n*n
    tmp = [0]*10
    for c in str(num):
        tmp[int(c)] += 1
    if memo[0] < tmp[0]: continue
    for i in range(1, 10):
        if memo[i] != tmp[i]: break
    else:
        ans += 1
print(ans)