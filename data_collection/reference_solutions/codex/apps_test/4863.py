import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    ans = data.split()[1:]
    return str(sum(a == b for a, b in zip(ans, ans[1:]))) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
