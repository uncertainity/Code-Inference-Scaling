import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    sides, rolls = map(int, data.split())
    exp = 0.0
    for _ in range(rolls):
        exp = sum(max(exp, roll) for roll in range(1, sides + 1)) / sides
    return str(exp).rstrip("0").rstrip(".") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
