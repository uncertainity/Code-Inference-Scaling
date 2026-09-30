import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    names = data.splitlines()[1:]
    if names == sorted(names):
        return "INCREASING\n"
    if names == sorted(names, reverse=True):
        return "DECREASING\n"
    return "NEITHER\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
