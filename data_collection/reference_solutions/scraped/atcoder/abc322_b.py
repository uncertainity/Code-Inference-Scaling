import bisect
import math
import sys
import copy
#import numpy as np # Pypyでは使えない
from collections import deque,defaultdict,Counter
from itertools import permutations,combinations,product,accumulate
from array import array # 連続メモリ上の配列（数値型で使用，高速）
# al=[chr(ord('a') + i) for i in range(26)]
# Al=[chr(ord('A') + i) for i in range(26)]
DEBUG = False  # デバッグ時は True、本番環境では False
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
x = list(map(int, input().split())) 
S = str(input())
T = str(input())       
N =x[0]
M =x[1]
if T[0:N] == S:
    if T[M-N:] ==S:
        print(0)
    else:
        print(1)
elif T[M-N:] ==S:
    print(2)
else:
    print(3)
#n = int(input())