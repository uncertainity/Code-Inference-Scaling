import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = data.split()[1:]
    ok = all(word == "mumble" or int(word) == i for i, word in enumerate(vals, 1))
    return ("makes sense" if ok else "something is fishy") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
