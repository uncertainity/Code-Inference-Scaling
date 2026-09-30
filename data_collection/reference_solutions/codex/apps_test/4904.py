import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    a = b = 0
    for i in range(0, len(s), 2):
        if s[i] == "A":
            a += int(s[i + 1])
        else:
            b += int(s[i + 1])
    return ("A" if a > b else "B") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
