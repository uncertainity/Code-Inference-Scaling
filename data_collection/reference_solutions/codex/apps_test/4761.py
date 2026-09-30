import sys


def valid(x):
    s = str(x)
    return "0" not in s and len(set(s)) == len(s) and all(x % int(d) == 0 for d in s)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lo, hi = map(int, data.split())
    return str(sum(valid(x) for x in range(lo, hi + 1))) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
