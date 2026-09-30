import sortedcontainers

N, M, D = list(map(int,input().split()))
A = sortedcontainers.SortedList(list(map(int,input().split())))
B = sortedcontainers.SortedList(list(map(int,input().split())))

answer = []
for i in range(N):
    a = B.bisect_left(A[i] - D)
    b = B.bisect_right(A[i] + D)
    if a < M and abs(A[i] - B[a]) <= D:
        answer.append(A[i] + B[a])
    if b > 0 and abs(A[i] - B[b - 1]) <= D:
        answer.append(A[i] + B[b - 1])

if len(answer) == 0:
    print(-1)
else:
    print(max(answer))