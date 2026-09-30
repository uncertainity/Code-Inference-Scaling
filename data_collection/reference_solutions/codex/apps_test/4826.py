import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return ("Alice" if int(data) % 2 else "Bob") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
