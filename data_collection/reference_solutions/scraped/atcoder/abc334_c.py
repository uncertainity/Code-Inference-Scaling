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
  a=L()
  sa=[]
  for i in range(k-1):
    sa.append(a[i+1]-a[i])
  ruimae=[0]
  ruiusi=[0]
  for i in range(0,len(sa),2):
    ruimae.append(ruimae[-1]+sa[i])
  for i in range(len(sa)-1,-1,-2):
    ruiusi.append(ruiusi[-1]+sa[i])
  ruiusi.reverse()
  if k%2 == 0:
    print(ruimae[-1])
    exit()
  ans=INF
  for i in range(0,k,2):
    ans=min(ans,ruimae[i//2]+ruiusi[i//2])
  print(ans)
  
solve()