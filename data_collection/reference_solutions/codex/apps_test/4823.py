import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(max(Counter(card[0] for card in data.split()).values())) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
