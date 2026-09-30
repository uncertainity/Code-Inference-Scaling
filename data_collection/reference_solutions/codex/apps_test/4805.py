import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words = data.split()
    return ("yes" if len(words) == len(set(words)) else "no") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
