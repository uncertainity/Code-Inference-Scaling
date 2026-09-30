import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, p, q = map(int, data.split())
    return ("paul" if ((p + q) // n) % 2 == 0 else "opponent") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
