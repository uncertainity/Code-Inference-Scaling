import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(round(float(data) * 1000 * 5280 / 4854)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
