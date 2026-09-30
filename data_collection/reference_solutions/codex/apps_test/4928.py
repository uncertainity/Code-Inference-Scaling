import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    return str((n // 2 + 1) * ((n + 1) // 2 + 1)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
