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
while N%2 == 0: N //= 2
while N%3 == 0: N //= 3
yn(N == 1)