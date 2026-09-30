import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()))
    r, n = nums[:2]
    booked = set(nums[2:])
    if 23 <= r and 23 not in booked:
        return "23\n"
    for room in range(1, r + 1):
        if room not in booked:
            return str(room) + "\n"
    return "too late\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
