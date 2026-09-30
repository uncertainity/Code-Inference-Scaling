import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(map(int, data.split()))
    t = next(it)
    out = []
    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]
        pos = min(range(n), key=a.__getitem__)
        a[pos] += 1
        prod = 1
        for x in a:
            prod *= x
        out.append(str(prod))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
