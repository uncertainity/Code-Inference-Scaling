import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(data.split())
    t = int(next(it))
    out = []
    for _ in range(t):
        s = next(it)
        bad = sum(a != b for a, b in zip(s, "abc"))
        out.append("YES" if bad <= 2 else "NO")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
