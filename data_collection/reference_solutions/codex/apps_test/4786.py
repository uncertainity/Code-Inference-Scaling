import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    keys = set()
    for line in data.splitlines()[1:]:
        keys.add(line.lower().replace("-", " "))
    return str(len(keys)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
