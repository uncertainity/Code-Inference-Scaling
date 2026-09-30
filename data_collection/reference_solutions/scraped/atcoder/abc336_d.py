N = int(input())
A = list(map(int, input().split()))

left = [0] * N
left[0] = 1
for i in range(1, N) :
    a = A[i]
    if left[i-1] + 1 <= a :
        left[i] = left[i-1] + 1
    else :
        left[i] = a

right = [0] * N
right[-1] = 1
for i in range(N-2, -1, -1) :
    a = A[i]
    if right[i+1] + 1 <= a :
        right[i] = right[i+1] + 1
    else :
        right[i] = a


ans = 0
for i in range(0, N) :
    ans = max(ans, min(left[i], right[i]))
print(ans)

