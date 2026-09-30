import sys


class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    if not nums:
        return ""
    k = nums[0]
    true_dsu = DSU()
    floor_dsu = DSU()
    true_cycle = False
    floor_cycle = False
    seen_floor_edges = set()
    p = 1
    for _ in range(k):
        x1, y1, z1, x2, y2, z2 = nums[p:p + 6]
        p += 6
        a3 = (x1, y1, z1)
        b3 = (x2, y2, z2)
        if not true_dsu.union(a3, b3):
            true_cycle = True
        a2 = (x1, y1)
        b2 = (x2, y2)
        if a2 != b2:
            edge = tuple(sorted((a2, b2)))
            if edge not in seen_floor_edges:
                seen_floor_edges.add(edge)
                if not floor_dsu.union(a2, b2):
                    floor_cycle = True
    out = []
    out.append("True closed chains" if true_cycle else "No true closed chains")
    out.append("Floor closed chains" if floor_cycle else "No floor closed chains")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
