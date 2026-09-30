import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n = vals[0]
    last = {}
    best = n
    for i, x in enumerate(vals[1:]):
        if x in last:
            best = min(best, i - last[x])
        last[x] = i
    return str(best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
