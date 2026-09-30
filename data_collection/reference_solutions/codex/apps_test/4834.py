import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    times = list(map(int, data.split()[1:]))
    total = sum(times)
    longest = max(times)
    return str(max(total, 2 * longest)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
