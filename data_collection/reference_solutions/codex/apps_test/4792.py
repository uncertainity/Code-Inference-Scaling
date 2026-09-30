import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    out = []
    for ch in s:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
