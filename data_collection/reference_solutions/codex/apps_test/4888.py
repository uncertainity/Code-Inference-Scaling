import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    n, limit = nums[0], nums[1]
    total = ans = 0
    for x in nums[2:2 + n]:
        if total + x > limit:
            break
        total += x
        ans += 1
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
