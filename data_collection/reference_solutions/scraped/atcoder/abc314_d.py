N = int(input())
S = input()
T = []
U = [i+1 for i in range(N)]
V = {i+1 for i in range(N)}
flag = 0
for i in S:
    T.append(ord(i))
Q = int(input())
for i in range(Q):
    A = list(input().split())
    if A[0] == "1":
        A[1] = int(A[1])
        T[A[1]-1] = ord(A[2])
        if A[1] not in V:
            V.add(A[1])
            U.append(A[1])
    else:
        flag = int(A[0])
        for j in U:
            T[j-1] %= 32
        U.clear()
        V.clear()

C = []

flag = abs(flag-3)+2
for i in T:
    if i < 32:
        C.append(chr(i+32*flag))
    else:
        C.append(chr(i))
ans = "".join(C)
print(ans)