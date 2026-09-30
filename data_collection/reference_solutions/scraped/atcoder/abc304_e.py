class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def root(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def merge(self, x, y):
        root_x = self.root(x)
        root_y = self.root(y)
        if root_x == root_y:
            return False
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def same(self, x, y):
        return self.root(x) == self.root(y)

# 入力
N, M = map(int, input().split())

# Union-Find を作る
uf = UnionFind(N)
for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    uf.merge(u, v)

# K 組の頂点対についての前処理
K = int(input())
x = [0] * K
y = [0] * K
S = set()
for i in range(K):
    x[i], y[i] = map(int, input().split())
    x[i] -= 1
    y[i] -= 1
    x[i] = uf.root(x[i])
    y[i] = uf.root(y[i])
    if x[i] > y[i]:
        x[i], y[i] = y[i], x[i]
    S.add((x[i], y[i]))

# クエリ処理
Q = int(input())
for _ in range(Q):
    p, q = map(int, input().split())
    p -= 1
    q -= 1
    p = uf.root(p)
    q = uf.root(q)
    if p > q:
        p, q = q, p
    
    if not uf.same(p, q) and (p, q) in S:
        print("No")
    else:
        print("Yes")