import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()[1:]))
    out = []
    best = -1
    for x in nums:
        if x > best:
            out.append(x)
            best = x
    return str(len(out)) + "\n" + " ".join(map(str, out)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
