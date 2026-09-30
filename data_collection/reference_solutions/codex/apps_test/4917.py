import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    intervals = [tuple(map(int, line.split())) for line in data.splitlines()[1:]]
    lo = max(a for a, _ in intervals)
    hi = min(b for _, b in intervals)
    return ("gunilla has a point" if lo <= hi else "edward is right") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
