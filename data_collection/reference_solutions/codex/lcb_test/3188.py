import ast
import sys


class Solution:
    def findChampion(self, grid) -> int:
        return max(range(len(grid)), key=lambda i: sum(grid[i]))


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().findChampion(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
