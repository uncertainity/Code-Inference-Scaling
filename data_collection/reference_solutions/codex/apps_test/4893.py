import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, p = vals[:2]
    cars = sorted(vals[2:2 + n])
    worst = 0
    for i, pos in enumerate(cars):
        worst = max(worst, p * (i + 1) + 1 - pos)
    return str(worst) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
