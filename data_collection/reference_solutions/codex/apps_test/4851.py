import sys


def digit_sum(x):
    return sum(map(int, str(x)))


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    while n % digit_sum(n):
        n += 1
    return str(n) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
