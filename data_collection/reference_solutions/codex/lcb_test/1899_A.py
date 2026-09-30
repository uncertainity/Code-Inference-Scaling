import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    return "".join("First\n" if n % 3 else "Second\n" for n in nums[1:])


if __name__ == "__main__":
    sys.stdout.write(solve())
