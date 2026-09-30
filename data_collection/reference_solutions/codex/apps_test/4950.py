import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    n = nums[0]
    best = 0
    for i in range(n - 1):
        t1, d1 = nums[1 + 2 * i], nums[2 + 2 * i]
        t2, d2 = nums[3 + 2 * i], nums[4 + 2 * i]
        best = max(best, (d2 - d1) // (t2 - t1))
    return str(best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
