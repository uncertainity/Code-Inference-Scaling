import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    out = []
    for line in data.splitlines()[1:]:
        if line.startswith("Simon says"):
            out.append(line[10:])
    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    sys.stdout.write(solve())
