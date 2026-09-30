import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    days = set()
    p = 1
    for _ in range(vals[0]):
        a, b = vals[p], vals[p + 1]
        p += 2
        days.update(range(a, b + 1))
    return str(len(days)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
