import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return "".join(str(len(x)) + "\n" for x in data.split()[1:])


if __name__ == "__main__":
    sys.stdout.write(solve())
