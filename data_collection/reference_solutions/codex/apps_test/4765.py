import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n = vals[0]
    items = [(vals[i], vals[i + 1]) for i in range(1, 2 * n, 2)]
    best = 10 ** 18
    for mask in range(1, 1 << n):
        sour = 1
        bitter = 0
        for i, (s, b) in enumerate(items):
            if mask >> i & 1:
                sour *= s
                bitter += b
        best = min(best, abs(sour - bitter))
    return str(best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
