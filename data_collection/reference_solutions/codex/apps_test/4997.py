import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    pos = 0
    cups = [1, 0, 0]
    for ch in data.strip():
        if ch == "A":
            cups[0], cups[1] = cups[1], cups[0]
        elif ch == "B":
            cups[1], cups[2] = cups[2], cups[1]
        else:
            cups[0], cups[2] = cups[2], cups[0]
    return str(cups.index(1) + 1) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
