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
        pref = [0]
        for x in a:
            pref.append(pref[-1] + x)
        ans = 0
        for k in range(1, n + 1):
            if n % k:
                continue
            sums = [pref[i + k] - pref[i] for i in range(0, n, k)]
            ans = max(ans, max(sums) - min(sums))
        out.append(str(ans))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
