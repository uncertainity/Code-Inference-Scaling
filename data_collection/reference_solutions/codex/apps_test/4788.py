import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b = map(int, data.split())
    diff = (b - a) % 360
    if diff > 180:
        diff -= 360
    return str(diff) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
