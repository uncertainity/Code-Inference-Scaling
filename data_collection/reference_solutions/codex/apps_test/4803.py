import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = float(data)
    return f"{n ** (1 / n):.6f}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
