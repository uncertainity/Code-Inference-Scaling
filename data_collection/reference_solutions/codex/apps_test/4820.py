import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, b = map(int, data.split())
    return ("yes" if n <= 2 ** (b + 1) - 1 else "no") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
