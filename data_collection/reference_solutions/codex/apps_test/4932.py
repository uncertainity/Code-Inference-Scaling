import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, c, d, *times = map(int, data.split())
    out = []
    for t in times:
        x = (t - 1) % (a + b) < a
        y = (t - 1) % (c + d) < c
        out.append(["none", "one", "both"][x + y])
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
