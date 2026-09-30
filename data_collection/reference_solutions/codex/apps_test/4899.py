import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return "h" + "e" * (2 * (len(data.strip()) - 2)) + "y\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
