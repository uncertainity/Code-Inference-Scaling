import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    x, y = map(int, data.split())
    if y == 1:
        return "ALL GOOD\n" if x == 0 else "IMPOSSIBLE\n"
    num = -x
    den = y - 1
    if num % den == 0:
        return str(num // den) + "\n"
    return f"{num / den:.9f}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
