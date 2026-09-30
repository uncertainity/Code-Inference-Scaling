import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b = data.split()
    return str(max(int(a[::-1]), int(b[::-1]))) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
