import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    parts = data.split()
    n = int(parts[0])
    stack = [0]
    i = 2
    while i < len(parts):
        if parts[i] == "undo":
            count = int(parts[i + 1])
            del stack[-count:]
            i += 2
        else:
            stack.append((stack[-1] + int(parts[i])) % n)
            i += 1
    return str(stack[-1]) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
