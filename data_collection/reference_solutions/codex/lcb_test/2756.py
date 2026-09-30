import ast
import sys


class Solution:
    def buyChoco(self, prices, money: int) -> int:
        a, b = sorted(prices)[:2]
        return money - a - b if a + b <= money else money


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = [line for line in data.splitlines() if line.strip()]
    return str(Solution().buyChoco(ast.literal_eval(lines[0]), int(lines[1])))


if __name__ == "__main__":
    sys.stdout.write(solve())
