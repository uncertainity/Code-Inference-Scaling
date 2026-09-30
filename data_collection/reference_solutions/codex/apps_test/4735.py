import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    year = int(data)
    month = 2018 * 12 + 3
    target_start = year * 12
    target_end = target_start + 12
    while month < target_end:
        if target_start <= month < target_end:
            return "yes\n"
        month += 26
    return "no\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
