import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    seedlings = sorted(nums[1:], reverse=True)
    return str(max(day + grow for day, grow in enumerate(seedlings, 1)) + 1) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
