import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b = data.split()
    return ("go" if len(a) >= len(b) else "no") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
