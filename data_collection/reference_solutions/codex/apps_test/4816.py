import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    x, y, x1, y1, x2, y2 = map(float, data.split())
    cx = min(max(x, x1), x2)
    cy = min(max(y, y1), y2)
    return str(math.hypot(x - cx, y - cy)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
