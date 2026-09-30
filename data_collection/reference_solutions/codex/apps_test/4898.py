import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    intervals = sorted(tuple(map(int, line.split())) for line in data.splitlines()[1:])
    ans = 0
    current = -1
    for start, end in intervals:
        if start > current:
            ans += 1
            current = end
        else:
            current = min(current, end)
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
