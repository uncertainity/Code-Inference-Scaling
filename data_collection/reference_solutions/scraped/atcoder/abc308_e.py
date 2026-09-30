from collections import defaultdict

N = int(input())
A = list(map(int, input().split()))
S = input()

leftM = defaultdict(int) # 現在見ているインデックスより左にある"M"に対応する数字とその個数
rightX = defaultdict(int) # 現在見ているインデックスより右にある"X"に対応する数字とその個数
for a, s in zip(A, S):
    if s == "X":
        rightX[a] += 1

def mex(*values):
    return min({0, 1, 2, 3} - set(values))

ans = 0
for a, s in zip(A, S): # "E"を中央とし、左側の"M"と右側の"R"の組み合わせについて考える
    if s == "X":
        rightX[a] -= 1
    elif s == "E":
        for km, vm in leftM.items():
            for kx, vx in rightX.items():
                ans += mex(km, a, kx) * (vm * vx) # 左側の"M"と右側の"X"の組み合わせは vm*vx 通り
    elif s == "M":
        leftM[a] += 1

print(ans)