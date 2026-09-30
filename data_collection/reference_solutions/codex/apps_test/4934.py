import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    h, v = map(int, data.split())
    return str(math.ceil(h / math.sin(math.radians(v)))) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
