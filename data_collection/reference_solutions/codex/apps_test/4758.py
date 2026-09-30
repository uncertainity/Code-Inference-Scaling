import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, c = map(int, data.split())
    return str(a * b * c) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
