import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    n, ships = nums[:2]
    ans = 0
    for need in sorted(nums[2:2 + n]):
        if ships > need:
            ships -= need + 1
            ans += 1
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
