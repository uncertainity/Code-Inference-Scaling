import bisect

N, M, P = list(map(int,input().split()))
A = list(map(int,input().split()))
B = list(map(int,input().split()))

A.sort()
B.sort()

Sa = [ 0 for _ in range(N)]
Sa[0] = A[0]
for i in range(1, N):
    Sa[i] = Sa[i - 1] + A[i]

answer = 0
for i in range(M):
    x = bisect.bisect(A, P - B[i])
    answer += P * (N - x)
    if x > 0:
        answer += Sa[x - 1] + (B[i] * x)
print(answer)