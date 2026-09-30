import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    _, w, h = nums[:3]
    limit = w * w + h * h
    return "".join(("DA" if x * x <= limit else "NE") + "\n" for x in nums[3:])


if __name__ == "__main__":
    sys.stdout.write(solve())
