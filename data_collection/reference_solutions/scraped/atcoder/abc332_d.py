import bisect
import math
import sys
sys.setrecursionlimit(10000000)
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

def tentou(p):
    s=[0]*len(p)
    ans=0
    for i in range(len(p)):
        ans+=sum(s[p[i]:])
        s[p[i]]+=1
    return ans

def solve():
    H,W=getNM()
    A=[getlist() for i in range(H)]
    B=[getlist() for i in range(H)]
    ans=[]
    for I in itertools.permutations(range(H)):
        for J in itertools.permutations(range(W)):
            f=True
            for i in range(H):
                s=I[i]
                for j in range(W):
                    t=J[j]
                    if A[s][t]!=B[i][j]:
                        f=False
                        break
                if not f:
                    break
            if f:
                ans.append(I)
                ans.append(J)
                break
        if ans:
            break
    if not ans:
        print(-1)
    else:
        p=tentou(ans[0])
        p+=tentou(ans[1])
        print(p)
    
    return
if __name__=='__main__':
    solve()
                
                    
    
            