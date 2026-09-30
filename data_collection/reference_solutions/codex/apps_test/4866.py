import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    return ("yup" if s in ("OCT 31", "DEC 25") else "nope") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
