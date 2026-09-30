import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    r, c = map(int, data.split())
    ans = ((r - c) ** 2 / (r * r)) * 100
    return (f"{ans:.9f}" if ans == 0 else f"{ans:.6f}") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
