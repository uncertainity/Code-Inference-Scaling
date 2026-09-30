import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, op, b = data.split()
    return str(int(a) + int(b) if op == "+" else int(a) * int(b)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
