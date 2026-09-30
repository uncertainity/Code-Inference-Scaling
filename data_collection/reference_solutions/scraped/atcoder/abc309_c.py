#LCM→最小公倍数、GCD→最大公約数
#from math import lcm,gcd,pi,isqrt
#from collections import deque
#from functools import cache
#from heapq import heappop,heappush
#from sortedcontainers import SortedList,SortedSet,SortedDict
#import bisect
#import itertools
import sys
input = lambda: sys.stdin.readline().rstrip()
#sys.setrecursionlimit(3000000)
move = ((1,0),(-1,0),(0,1),(0,-1))
def I(): return int(input())
def L(): return list(map(int,input().split()))
def M(): return map(int,input().split())
def LL(n): return [L() for _ in range(n)]
def S(): return list(input())
def GD(h): return [S() for i in range(h)]
def PY(): return print("Yes")
def PN(): return print("No")
def PJ(x): return print("".join(x))
INF=10**18

def solve():
  n,k=M()
  eve=[]
  now=0
  for i in range(n):
    a,b=M()
    now+=b
    eve.append([a+1,b])
  eve.sort(reverse=True)
  if now <= k:
    print(1)
    exit()
  hi=0
  while now > k:
    a,b=eve.pop()
    now-=b
    hi=a
  print(hi)
  
  
  
solve()