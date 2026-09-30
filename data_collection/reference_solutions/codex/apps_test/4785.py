import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return ("hiss" if "ss" in data.strip() else "no hiss") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
