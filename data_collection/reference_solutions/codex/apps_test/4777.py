import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b = 1, 0
    for _ in range(int(data)):
        a, b = b, a + b
    return f"{a} {b}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
