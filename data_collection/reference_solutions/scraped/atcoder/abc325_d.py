import sys
from sys import stdin, setrecursionlimit
from math import gcd, lcm, perm, comb, sqrt
import heapq as hq
from types import GeneratorType
def ceil(x): return int(x) if(x == int(x)) else int(x)+1
def ceildiv(x, d): return x//d if(x % d == 0) else x//d+1
MOD = 1_000_000_007
# setrecursionlimit(10**6)
input = lambda: stdin.readline().strip()
######### main code goes here #########

n = int(input())
items = []
for _ in range(n):
    T, D = map(int, input().split())
    items.append((T, T + D))
items.sort()

heap = []
idx = 0
cur_time = 0
count = 0
while idx < n or heap:
    if not heap and idx < n:
        cur_time = items[idx][0]
    while idx < n and items[idx][0] <= cur_time:
        hq.heappush(heap, items[idx][1])
        idx += 1
    while heap and heap[0] < cur_time:
        hq.heappop(heap)
    if heap:
        hq.heappop(heap)
        count += 1
        cur_time += 1

print(count)