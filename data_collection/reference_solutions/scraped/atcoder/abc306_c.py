N = int(input())
A = [int(x) - 1 for x in input().split()]

pos = [-1] * N
cen = [-1] * N
for i in range(N * 3):
    if pos[A[i]] == -1:
        pos[A[i]] = i
    elif cen[A[i]] == -1:
        cen[A[i]] = i

B = sorted((cen[i], i + 1) for i in range(N))
for _, i in B:
    print(i)
