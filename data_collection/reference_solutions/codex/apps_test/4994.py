import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    xs = Counter(nums[::2])
    ys = Counter(nums[1::2])
    x = next(k for k, v in xs.items() if v == 1)
    y = next(k for k, v in ys.items() if v == 1)
    return f"{x} {y}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
