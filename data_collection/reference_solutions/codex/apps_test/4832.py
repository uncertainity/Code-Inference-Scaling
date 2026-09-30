import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    r = int(data)
    return f"{math.pi * r * r:.6f}\n{2 * r * r:.6f}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
