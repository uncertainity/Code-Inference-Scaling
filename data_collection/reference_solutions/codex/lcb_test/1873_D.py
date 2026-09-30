import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    it = iter(data.split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        s = next(it)
        ans = i = 0
        while i < n:
            if s[i] == "B":
                ans += 1
                i += k
            else:
                i += 1
        out.append(str(ans))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
