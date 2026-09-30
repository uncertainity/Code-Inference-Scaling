import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    h, m = map(int, data.split())
    t = (h * 60 + m - 45) % (24 * 60)
    return f"{t // 60} {t % 60}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
