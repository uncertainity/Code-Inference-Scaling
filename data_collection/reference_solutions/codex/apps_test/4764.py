import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, h, v = map(int, data.split())
    return str(max(h, n - h) * max(v, n - v) * 4) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
