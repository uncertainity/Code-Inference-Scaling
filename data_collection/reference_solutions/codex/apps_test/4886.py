import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, k = map(int, data.split())
    return ("Your wish is granted!" if n <= 2 ** k else "You will become a flying monkey!") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
