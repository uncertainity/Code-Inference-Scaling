import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    total_m, total_s = 0, 0
    for i in range(vals[0]):
        total_m += vals[1 + 2 * i]
        total_s += vals[2 + 2 * i]
    ratio = total_s / (60 * total_m)
    return f"{ratio:.9f}\n" if ratio > 1 else "measurement error\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
