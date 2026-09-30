import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    total = 1
    while n != 1:
        total += n
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return str(total) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
