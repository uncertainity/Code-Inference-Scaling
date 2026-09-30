import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(map(int, data.split()))
    t = next(it)
    out = []
    for _ in range(t):
        n = next(it)
        k = next(it)
        a = [next(it) for _ in range(n)]
        if k == 4:
            make_one = min((4 - x % 4) % 4 for x in a)
            evens = sum(x % 2 == 0 for x in a)
            out.append(str(min(make_one, max(0, 2 - evens))))
        else:
            out.append(str(min((k - x % k) % k for x in a)))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
