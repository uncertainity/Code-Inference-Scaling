import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    n = len(s)
    r = max(i for i in range(1, n + 1) if n % i == 0 and i <= n // i)
    c = n // r
    return "".join(s[i + j * r] for i in range(r) for j in range(c)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
