import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    area, perimeter = map(float, data.split())
    return ("Diablo is happy!" if perimeter >= 2 * math.sqrt(math.pi * area) else "Need more materials!") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
