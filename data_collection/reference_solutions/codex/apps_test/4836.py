import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, capacity = vals[:2]
    a = vals[2:2 + n]
    best = 0
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += a[j]
            if total <= capacity:
                best = max(best, j - i + 1)
            else:
                break
    return str(best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
