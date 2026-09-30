import sys
from collections import deque


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    f, s, g, u, d = map(int, data.split())
    dist = [-1] * (f + 1)
    q = deque([s])
    dist[s] = 0
    while q:
        x = q.popleft()
        if x == g:
            return str(dist[x]) + "\n"
        for y in (x + u, x - d):
            if 1 <= y <= f and dist[y] < 0:
                dist[y] = dist[x] + 1
                q.append(y)
    return "use the stairs\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
