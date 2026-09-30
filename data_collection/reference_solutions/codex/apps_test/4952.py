import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    names = [line for line in data.splitlines() if line != "***"]
    cnt = Counter(names)
    best = max(cnt.values())
    winners = [name for name, c in cnt.items() if c == best]
    return (winners[0] if len(winners) == 1 else "Runoff!") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
