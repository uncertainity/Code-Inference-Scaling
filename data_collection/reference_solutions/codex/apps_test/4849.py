import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    out = [str(i + 1) for i, line in enumerate(lines[:5]) if "FBI" in line]
    return (" ".join(out) if out else "HE GOT AWAY!") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
