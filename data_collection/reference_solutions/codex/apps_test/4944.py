import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    days = printers = 1
    while printers < n:
        printers *= 2
        days += 1
    return str(days) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
