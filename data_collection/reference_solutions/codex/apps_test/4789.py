import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()[1:]))
    ans = 1
    for a, b in zip(nums, nums[1:]):
        if b < a:
            ans += 1
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
