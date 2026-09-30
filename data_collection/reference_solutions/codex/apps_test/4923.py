import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    rolls = vals[1:]
    cnt = Counter(rolls)
    for value in range(6, 0, -1):
        if cnt[value] == 1:
            return str(rolls.index(value) + 1) + "\n"
    return "none\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
