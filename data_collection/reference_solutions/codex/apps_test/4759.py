import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    good = [x for x in vals[1:] if x != -1]
    return str(sum(good) / len(good)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
