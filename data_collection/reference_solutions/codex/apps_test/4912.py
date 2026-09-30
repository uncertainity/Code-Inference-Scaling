import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    h, w, n = nums[:3]
    rows = width = 0
    for b in nums[3:3 + n]:
        width += b
        if width == w:
            rows += 1
            width = 0
            if rows == h:
                return "YES\n"
        elif width > w:
            return "NO\n"
    return "NO\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
