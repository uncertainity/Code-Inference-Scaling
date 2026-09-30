import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    r, c = map(int, lines[0].split())
    grid = lines[1:]
    ans = [0] * 5
    for i in range(r - 1):
        for j in range(c - 1):
            block = [grid[i][j], grid[i + 1][j], grid[i][j + 1], grid[i + 1][j + 1]]
            if "#" not in block:
                ans[block.count("X")] += 1
    return "\n".join(map(str, ans)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
