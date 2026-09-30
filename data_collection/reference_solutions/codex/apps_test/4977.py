import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, c, d, t = map(int, data.split())
    dist = abs(a - c) + abs(b - d)
    return ("Y" if dist <= t and (t - dist) % 2 == 0 else "N") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
