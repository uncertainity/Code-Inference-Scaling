import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return ("1" if data.strip().startswith("555") else "0") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
