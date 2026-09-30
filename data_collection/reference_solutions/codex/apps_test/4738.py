import sys


def rotate(s):
    return s[-1] + s[:-1]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    n = len(s)
    for k in range(1, n + 1):
        if n % k:
            continue
        blocks = [s[i:i + k] for i in range(0, n, k)]
        if all(blocks[i] == rotate(blocks[i - 1]) for i in range(1, len(blocks))):
            return str(k) + "\n"
    return str(n) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
