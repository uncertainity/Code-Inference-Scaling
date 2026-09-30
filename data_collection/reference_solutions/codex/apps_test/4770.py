import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, m = map(int, data.split())
    diff = abs(n - m)
    word = "piece" if diff == 1 else "pieces"
    if n < m:
        return f"Dr. Chaz will have {diff} {word} of chicken left over!\n"
    return f"Dr. Chaz needs {diff} more {word} of chicken!\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
