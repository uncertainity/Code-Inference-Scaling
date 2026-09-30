import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    x, y, n = map(int, data.split())
    out = []
    for i in range(1, n + 1):
        s = ""
        if i % x == 0:
            s += "Fizz"
        if i % y == 0:
            s += "Buzz"
        out.append(s or str(i))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
