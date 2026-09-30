import sys

input = sys.stdin.buffer.readline

write = sys.stdout.write

class FenwickTree:

    def __init__(self, n):
        self.n = n + 1
        self.tree = [0]*self.n


    def build(self, data):
        for i in range(1, self.n):
            self.tree[i] += data[i-1]
            j = i + (i&-i)
            if j < self.n:
                self.tree[j] += self.tree[i]


    def add(self, i, x):
        i += 1
        while i < self.n:
            self.tree[i] += x
            i += i & -i


    def bisect(self):
        d = 1<<((self.n-1).bit_length())
        i = 0
        while d > 0:
            if i + d < self.n and self.tree[i+d] == d:
                i += d
            d >>= 1
        return i


N, Q = map(int, input().split())

A = list(map(int, input().split()))

cnt = [0]*N
for ai in A:
    if ai < N:
        cnt[ai] += 1


bit = FenwickTree(N+1)
B = [0]*(N+1)
for i in range(N):
    if cnt[i] > 0:
        B[i] = 1

bit.build(B)

ans = []
for _ in range(Q):
    i, x = map(int, input().split())
    i -= 1
    if A[i] < N:
        cnt[A[i]] -= 1
        if cnt[A[i]] == 0:
            bit.add(A[i], -1)
    A[i] = x
    if A[i] < N:
        if cnt[A[i]] == 0:
            bit.add(A[i], 1)
        cnt[A[i]] += 1
    ans.append(bit.bisect())


write("\n".join(map(str, ans)))