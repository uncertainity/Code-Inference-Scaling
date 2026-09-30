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
        best = cur = a[0]
        for i in range(1, n):
            if (a[i] & 1) != (a[i - 1] & 1):
                cur = max(a[i], cur + a[i])
            else:
                cur = a[i]
            best = max(best, cur)
        out.append(str(best))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
