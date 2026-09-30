from collections import defaultdict
from itertools import product

N = int(input())
R = input()
C = input()

def f(r, arr, first, cnt): # r行目、現在の文字列arr、先頭文字first、各文字の出現回数cnt
    if len(arr) == N:
        if cnt["A"] == cnt["B"] == cnt["C"] == 1: # 条件を満たす文字列ができたら、r行目の候補に追加
            rows[r].append(arr[:])
        return
    
    if cnt[first] == 0: # まだfirstを使っていない場合
        for x in [first, "."]:
            arr.append(x)
            cnt[x] += 1
            f(r, arr, first, cnt)
            arr.pop()
            cnt[x] -= 1
    else: # 既にfirstを使った場合
        candidates = ["A", "B", "C", "."]
        candidates.remove(first)
        for x in candidates:
            if x == ".":
                pass
            elif cnt[x] == 1:
                continue
            arr.append(x)
            cnt[x] += 1
            f(r, arr, first, cnt)
            arr.pop()
            cnt[x] -= 1

rows = [[] for _ in range(N)] # 各行について、条件を満たす文字列を全列挙
for r in range(N):
    f(r, [], first=R[r], cnt=defaultdict(int))

for P in product(*rows):
    for j in range(N): # 各列についても条件を満たすか確かめる
        first = None
        cnt = defaultdict(int)
        for i in range(N):
            if P[i][j] != ".":
                cnt[P[i][j]] += 1
                if first is None:
                    first = P[i][j]
        if first != C[j]:
            break
        if not (cnt["A"] == cnt["B"] == cnt["C"] == 1):
            break
    else:
        print("Yes")
        for row in P:
            print("".join(row))
        break
else:
    print("No")