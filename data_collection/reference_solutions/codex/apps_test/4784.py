import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    x, n = nums[0], nums[1]
    return str(x * (n + 1) - sum(nums[2:])) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
