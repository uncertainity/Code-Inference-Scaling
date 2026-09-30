import sys

input = sys.stdin.buffer.readline

write = sys.stdout.write

def left(n, k):
    return n*pow(2, k)

def kth_p(n, k):
    return n // pow(2, k)


def solve(N, X, K):
    if K == 0:
        return 1
    ans = 0
    D = N.bit_length()
    d = X.bit_length()
    K = min(K, 2*D + 2)
    if d > K:
        ans += 1
    if d + K <= D:
        ans += min(1<<K, max(0, N - left(X, K) + 1))
    for i in range(1, D+1):
        x = K - abs(i - d)
        if x <= 0 or x % 2 == 1:
            continue
        x //= 2
        y = x + abs(i - d)
        if i < d:
            u = kth_p(X, y)
            if u <= 0:
                continue
            ans += 1<<(x-1)
        else:
            u = kth_p(X, x)
            if u <= 0:
                continue
            if (X>>(x-1)) & 1:
                v = 2*u
            else:
                v = 2*u + 1
            ans += min(1<<(y-1), max(0, N - left(v, y-1) + 1))
    return ans


ans = []

for _ in range(int(input())):
    ans.append(solve(*list(map(int, input().split()))))


write("\n".join(map(str, ans)))