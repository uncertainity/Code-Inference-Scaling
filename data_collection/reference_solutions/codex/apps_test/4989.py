import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = sorted(map(int, data.split()[1:]), reverse=True)
    a = sum(nums[::2])
    b = sum(nums[1::2])
    return f"{a} {b}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
