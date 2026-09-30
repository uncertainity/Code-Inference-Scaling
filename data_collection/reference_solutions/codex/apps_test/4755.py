import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    c, k = map(int, data.split())
    p = 10 ** k
    return str((c + p // 2) // p * p) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
