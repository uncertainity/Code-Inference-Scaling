import bisect
import math
import sys
sys.setrecursionlimit(1000000)
import copy
import itertools
import heapq
from sortedcontainers import SortedDict,SortedSet,SortedList
import atcoder
from atcoder.dsu import DSU
#import numpy as np # Pypyでは使えない
from collections import deque,defaultdict,Counter
from itertools import permutations,combinations,product,accumulate
from array import array # 連続メモリ上の配列（数値型で使用，高速）
# al=[chr(ord('a') + i) for i in range(26)]
# Al=[chr(ord('A') + i) for i in range(26)]
INF = 602*pow(10,15)
import sys
from collections import defaultdict

def getN():
    return int(input())
def getNM():
    return map(int,input().split())
def getlist():
    return list(map(int,input().split()))
def getarray(N):
    return [getN() for _ in range(N)]
def getstr():
    return list(input())
#tree = DSU(N)
#from atcoder.lazysegtree import LazySegTree
from decimal import Decimal
tateyoko=[(-1,0),(1,0),(0,1),(0,-1)]
##インタラクティブなときは外す
input = sys.stdin.readline
##
read=sys.stdin.read
mod=998244353
def solve():
    
    N,M,K=getNM()
    d=[]
    for i in range(M):
        u,v,w=getNM()
        d.append((u-1,v-1,w))
    ans=INF
    for l in itertools.combinations([i for i in range(M)],N-1):
        tree=DSU(N)
        now=0
        f=True
        for i in range(N-1):
            t=l[i]
            u,v,w=d[t]
            if tree.same(u,v):
                f=False
                break
            tree.merge(u,v)
            now+=w
        if f:
            ans=min(ans,now%K)
    print(ans)
    
    
    return
if __name__=='__main__':
    solve()
                
                    
    
            