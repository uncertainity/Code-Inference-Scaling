import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    return str(1 if s.count("W") == s.count("B") else 0) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
