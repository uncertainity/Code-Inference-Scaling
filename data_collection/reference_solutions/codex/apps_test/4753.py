import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    return str(math.comb(n, 4)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
