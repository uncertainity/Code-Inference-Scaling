import sys


def seconds(s):
    h, m, sec = map(int, s.split(":"))
    return h * 3600 + m * 60 + sec


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b = data.split()
    diff = (seconds(b) - seconds(a)) % 86400
    if diff == 0:
        diff = 86400
    return f"{diff // 3600:02d}:{diff % 3600 // 60:02d}:{diff % 60:02d}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
