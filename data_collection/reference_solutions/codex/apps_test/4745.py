import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, limit = vals[:2]
    a = sorted(vals[2:2 + n])
    ans = 1
    for i in range(1, n):
        if a[i - 1] + a[i] <= limit:
            ans = i + 1
        else:
            break
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
