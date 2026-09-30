import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()[1:]
    ans = 0.0
    for i, line in enumerate(lines, 1):
        _, prob = line.split()
        ans += i * float(prob)
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
