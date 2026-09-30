import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, i = map(int, data.split())
    return str(a * (i - 1) + 1) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
