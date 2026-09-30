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
  ha,wa=M()
  a=[]
  for i in range(ha):
    s=S()
    if not a:
      if s.count("#") != 0:
        a.append(s)
    else:
      a.append(s)
  while True:
    if a[-1].count("#") != 0:
      break
    a.pop()
  while True:
    cou=0
    for i in range(len(a)):
      if a[i][0] == "#":
        cou+=1
    if cou == 0:
      for i in range(len(a)):
        a[i].pop(0)
    else:
      break
  while True:
    cou=0
    for i in range(len(a)):
      if a[i][-1] == "#":
        cou+=1
    if cou == 0:
      for i in range(len(a)):
        a[i].pop()
    else:
      break
  hb,wb=M()
  b=list()
  for i in range(hb):
    s=S()
    if not b:
      if s.count("#") != 0:
        b.append(s)
    else:
      b.append(s)
  while True:
    if b[-1].count("#") != 0:
      break
    b.pop()
  while True:
    cou=0
    for i in range(len(b)):
      if b[i][0] == "#":
        cou+=1
    if cou == 0:
      for i in range(len(b)):
        b[i].pop(0)
    else:
      break
  while True:
    cou=0
    for i in range(len(b)):
      if b[i][-1] == "#":
        cou+=1
    if cou == 0:
      for i in range(len(b)):
        b[i].pop()
    else:
      break
  hx,wx=M()
  x=GD(hx)
  #print(a)
  #print(b)
  for i in range(hx):
    for j in range(wx):
      new=[["."]*wx for i in range(hx)]
      if i+len(a) <= hx and j+len(a[0]) <= wx:
        for k in range(len(a)):
          for l in range(len(a[k])):
            new[i+k][j+l]=a[k][l]
        for k in range(hx):
          for l in range(wx):
            if k+len(b) <= hx and l+len(b[0]) <= wx:
              t=[new[i][:] for i in range(hx)]
              for m in range(len(b)):
                for n in range(len(b[0])):
                  if t[k+m][l+n] != "#":
                    t[k+m][l+n]=b[m][n]
              if t == x:
                PY()
                exit()
  PN()
            
solve()