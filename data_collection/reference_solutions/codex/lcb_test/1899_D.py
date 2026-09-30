import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(map(int, data.split()))
    t = next(it)
    out = []
    for _ in range(t):
        n = next(it)
        cnt = Counter(next(it) for _ in range(n))
        ans = sum(v * (v - 1) // 2 for v in cnt.values())
        ans += cnt[1] * cnt[2]
        out.append(str(ans))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
