import sys
from fractions import Fraction


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    f = Fraction(data.strip())
    c = (f - 32) * Fraction(5, 9)
    return f"{c.numerator}/{c.denominator}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
