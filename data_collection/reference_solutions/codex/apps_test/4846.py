import sys


def digit_sum(x):
    return sum(map(int, str(x)))


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    l, d, x = map(int, data.split())
    low = next(i for i in range(l, d + 1) if digit_sum(i) == x)
    high = next(i for i in range(d, l - 1, -1) if digit_sum(i) == x)
    return f"{low}\n{high}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
