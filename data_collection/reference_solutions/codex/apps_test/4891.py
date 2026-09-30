import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    have = list(map(int, data.split()))
    need = [1, 1, 2, 2, 2, 8]
    return " ".join(str(b - a) for a, b in zip(have, need)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
