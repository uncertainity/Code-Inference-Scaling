import sys
from decimal import Decimal, getcontext


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    getcontext().prec = 50
    ans = (Decimal(data.strip()).sqrt() * 4)
    return format(ans, ".20f").rstrip("0").rstrip(".") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
