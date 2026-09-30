from atcoder.fenwicktree import FenwickTree

N, Q = map(int, input().split())
S = input()

BIT = FenwickTree(N) # BIT[i]: i-1文字目とi文字目の間は条件を満たすか（10または01の並びであるか）
for i in range(N):
    if i == 0: # 先頭は必ず満たす
        BIT.add(i, 1)
    else:
        if S[i - 1] == S[i]:
            BIT.add(i, 0)
        else:
            BIT.add(i, 1)

for _ in range(Q):
    com, l, r = map(int, input().split())
    l -= 1
    r -= 1
    if com == 1: # 区間をビット反転するときは、l番目とr+1番目だけを更新すればよい
        if l != 0:
            a = 1 if BIT.sum(l, l + 1) == 0 else -1
            BIT.add(l, a)
        if r + 1 < N:
            a = 1 if BIT.sum(r + 1, r + 2) == 0 else -1
            BIT.add(r + 1, a)
    elif com == 2:
        if BIT.sum(l + 1, r + 1) == r - l:
            print("Yes")
        else:
            print("No")