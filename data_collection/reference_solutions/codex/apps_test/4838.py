import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    if nums[0] % 2:
        return "still running\n"
    return str(sum(nums[i + 1] - nums[i] for i in range(1, len(nums), 2))) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
