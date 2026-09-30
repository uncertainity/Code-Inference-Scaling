import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    c = Counter(data.strip())
    return str(c["T"] ** 2 + c["C"] ** 2 + c["G"] ** 2 + 7 * min(c["T"], c["C"], c["G"])) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
