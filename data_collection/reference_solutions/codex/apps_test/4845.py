import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    d, m = map(int, data.split())
    days = ["Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"]
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return days[(sum(month[:m - 1]) + d - 1) % 7] + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
