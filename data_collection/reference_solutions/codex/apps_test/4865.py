import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = data.split()
    t = int(vals[0])
    out = []
    p = 1
    for _ in range(t):
        mode = vals[p]
        minutes = int(vals[p + 1])
        h = int(vals[p + 2])
        m = int(vals[p + 3])
        p += 4
        cur = h * 60 + m + (minutes if mode == "F" else -minutes)
        cur %= 24 * 60
        out.append(f"{cur // 60} {cur % 60}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
