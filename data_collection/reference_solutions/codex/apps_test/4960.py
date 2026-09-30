import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    pad = (-len(s)) % 3
    s = "0" * pad + s
    return "".join(str(int(s[i:i + 3], 2)) for i in range(0, len(s), 3)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
