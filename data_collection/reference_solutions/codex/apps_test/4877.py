import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, h = map(int, data.split())
    day = 0
    pos = 0
    while True:
        day += 1
        pos += a
        if pos >= h:
            return str(day) + "\n"
        pos -= b


if __name__ == "__main__":
    sys.stdout.write(solve())
