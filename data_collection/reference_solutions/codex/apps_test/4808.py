import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    n, dm = nums[0], nums[1]
    for i, x in enumerate(nums[2:2 + n]):
        if x <= dm:
            return f"It hadn't snowed this early in {i} years!\n"
    return "It had never snowed this early!\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
