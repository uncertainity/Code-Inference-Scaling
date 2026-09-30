import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(data.split())
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)
        k = int(next(it))
        s = next(it)
        odd = sum(v % 2 for v in Counter(s).values())
        out.append("YES" if odd <= k + 1 else "NO")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
