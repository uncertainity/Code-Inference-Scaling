import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    return str(sum((x // 10) ** (x % 10) for x in nums[1:])) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
