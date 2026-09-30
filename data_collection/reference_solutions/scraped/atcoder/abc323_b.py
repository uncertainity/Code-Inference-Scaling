import bisect
import math
import sys
import copy
#import numpy as np # Pypyでは使えない
from collections import deque,defaultdict,Counter
from itertools import permutations,combinations,product,accumulate
from array import array # 連続メモリ上の配列（数値型で使用，高速）
# al=[chr(ord('a') + i) for i in range(26)]

from operator import itemgetter# Al=[chr(ord('A') + i) for i in range(26)]
DEBUG = False  # デバッグ時は True、本番環境では False
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
N = int(input())
total_score = []
result=[]
for i in range(N):
    score = list(str(input()))
    total_score.append((i+1,score.count("o")))
sorted_total_socre = sorted(total_score,key=itemgetter(1),reverse=True)  
for i in sorted_total_socre:
    result.append(str(i[0]))
print(" ".join(result))

#n = int(input())