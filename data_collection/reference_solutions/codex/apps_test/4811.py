import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    k = int(data)
    size = 1
    while size < k:
        size *= 2
    pieces = 0
    rem = k
    part = size
    while rem:
        if rem >= part:
            rem -= part
        else:
            part //= 2
            pieces += 1
    return f"{size} {pieces}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
