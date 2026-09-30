import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, p = map(int, data.splitlines()[0].split())
    return str(p) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
