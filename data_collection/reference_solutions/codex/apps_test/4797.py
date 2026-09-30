import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    stack = []
    for ch in data.strip():
        if ch == "<":
            if stack:
                stack.pop()
        else:
            stack.append(ch)
    return "".join(stack) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
