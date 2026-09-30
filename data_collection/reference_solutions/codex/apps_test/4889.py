import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    return str(sum(nums[1:]) - (nums[0] - 1)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
