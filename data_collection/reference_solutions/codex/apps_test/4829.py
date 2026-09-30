import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    l, r = map(int, data.split())
    if l == r == 0:
        return "Not a moose\n"
    kind = "Even" if l == r else "Odd"
    return f"{kind} {2 * max(l, r)}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
