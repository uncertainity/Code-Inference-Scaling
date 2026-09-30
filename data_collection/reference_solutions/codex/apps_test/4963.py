import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    n = nums[0]
    ans = [1] * n
    for person, before in enumerate(nums[1:], 2):
        ans[before + 1] = person
    return " ".join(map(str, ans)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
