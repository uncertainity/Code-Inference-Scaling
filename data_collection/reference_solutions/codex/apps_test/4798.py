import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return "".join(part[0] for part in data.strip().split("-")) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
