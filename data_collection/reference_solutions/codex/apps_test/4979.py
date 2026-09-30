import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(int(bin(int(data))[2:][::-1], 2)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
