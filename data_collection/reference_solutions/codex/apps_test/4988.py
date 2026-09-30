import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    out = []
    for x in map(int, data.split()[1:]):
        out.append(str(math.factorial(min(x, 5)) % 10))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
