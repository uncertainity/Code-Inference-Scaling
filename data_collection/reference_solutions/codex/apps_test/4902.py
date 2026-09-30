import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    odd = sum(v % 2 for v in Counter(data.strip()).values())
    return str(max(0, odd - 1)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
