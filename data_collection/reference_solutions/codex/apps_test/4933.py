import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a = sorted(map(int, data.split()))
    d1, d2 = a[1] - a[0], a[2] - a[1]
    if d1 == d2:
        ans = a[2] + d1
    elif d1 < d2:
        ans = a[1] + d1
    else:
        ans = a[0] + d2
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
