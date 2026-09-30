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
N = x[0]
M = x[1]
score_list = list(map(int, input().split()))
sorted_total_score = sorted(score_list,reverse=True)
total_score=[]   
max_score = 0
for i in range(N):
    own_score_list = list(str(input()))
    own_score = int(i+1)
    own_unsolved = []
    for t in range(M):
        if own_score_list[t] == "o":
            own_score += int(score_list[t])
        else:
            own_unsolved.append(int(score_list[t]))
    if own_score > max_score:
        max_score = own_score
    total_score.append((i+1,own_score,sorted(own_unsolved,reverse=True)))
for i in total_score:
    object_num = 0
    husoku = 0
    for t in i[2]:
        if  i[1] + husoku < max_score:
            object_num += 1
            husoku += t
        else:
            break
    print(object_num)


#n = int(input())