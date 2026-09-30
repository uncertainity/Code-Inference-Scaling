import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(len({int(x) % 42 for x in data.split()})) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
