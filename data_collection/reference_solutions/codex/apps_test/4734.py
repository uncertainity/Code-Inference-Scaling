import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    y, p = data.split()
    if y.endswith("ex"):
        return y + p + "\n"
    if y.endswith("e"):
        return y + "x" + p + "\n"
    if y[-1] in "aiou":
        return y[:-1] + "ex" + p + "\n"
    return y + "ex" + p + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
