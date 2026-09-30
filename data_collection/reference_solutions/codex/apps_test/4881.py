import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    if n % 2:
        return "Either\n"
    return ("Even" if n % 4 == 0 else "Odd") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
