import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n = vals[0]
    pts = [(vals[i], vals[i + 1]) for i in range(1, 2 * n, 2)]
    rows = set()
    cols = set()
    d1 = set()
    d2 = set()
    for r, c in pts:
        rows.add(r)
        cols.add(c)
        d1.add(r - c)
        d2.add(r + c)
    ok = len(rows) == len(cols) == len(d1) == len(d2) == n
    return ("CORRECT" if ok else "INCORRECT") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
