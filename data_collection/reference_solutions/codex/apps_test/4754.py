import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    socks = list(map(int, data.split()[1:]))
    stack = []
    moves = 0
    for sock in socks:
        stack.append(sock)
        moves += 1
        while len(stack) >= 2 and stack[-1] == stack[-2]:
            stack.pop()
            stack.pop()
    return ("impossible" if stack else str(moves)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
