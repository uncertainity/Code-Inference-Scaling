import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    r1, s = map(int, data.split())
    return str(2 * s - r1) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
