import sys
from itertools import permutations
input = sys.stdin.readline

# N = int(input())
# N, k = map(int, input().split())
# P = list(map(int, input().split()))
A = []
for _ in range(3):
    A.extend(list(map(int, input().split())))

ret = 0
cnt = 0
for iter in permutations(range(9)):
    cnt += 1
    # P = [A[i] for i in iter]
    R = [[] for _ in range(3)]
    C = [[] for _ in range(3)]
    X = [[] for _ in range(2)] 

    for i in iter:
        R[i//3].append(A[i])
        C[i%3].append(A[i])
        if i in [0, 4, 8]: X[0].append(A[i])
        if i in [6, 4, 2]: X[1].append(A[i])
    
    flag = 1
    for lst in R+C+X:
        if lst[0] == lst[1]:
            flag = 0
            break
    ret += flag



print(ret/cnt)

# 0 1 2
# 3 4 5
# 6 7 8