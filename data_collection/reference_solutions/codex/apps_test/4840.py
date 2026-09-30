import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    g = sum(vals[:4])
    e = sum(vals[4:])
    return ("Gunnar" if g > e else "Emma" if e > g else "Tie") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
