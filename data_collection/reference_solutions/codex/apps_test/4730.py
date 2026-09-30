import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    s = lines[1] if len(lines) > 1 else ""
    stack = []
    match = {")": "(", "]": "[", "}": "{"}
    for i, ch in enumerate(s):
        if ch in "([{":
            stack.append(ch)
        elif ch in match:
            if not stack or stack.pop() != match[ch]:
                return f"{ch} {i}\n"
    return "ok so far\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
