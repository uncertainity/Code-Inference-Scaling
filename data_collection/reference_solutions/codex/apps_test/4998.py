import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a = sorted(map(int, data.split()))
    return str(a[0] * a[2]) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
