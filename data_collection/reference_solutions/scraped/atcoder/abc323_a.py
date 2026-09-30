from itertools import permutations,combinations,product,accumulate
from array import array # 連続メモリ上の配列（数値型で使用，高速）
# al=[chr(ord('a') + i) for i in range(26)]
# Al=[chr(ord('A') + i) for i in range(26)]
DEBUG = False  # デバッグ時は True、本番環境では False
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
S = str(input()) 
checker = True  
str_list = list(S)
for i in range(1,16,2):
    if int(str_list[i]) == 1:
        checker = False
        break
if checker == True:
    print("Yes")
else:
    print("No")

#n = int(input())