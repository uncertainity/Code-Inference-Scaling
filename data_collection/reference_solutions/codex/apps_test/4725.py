import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    counts = sorted(Counter(data.strip()).values(), reverse=True)
    return str(sum(counts[2:])) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
