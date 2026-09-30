import ast
import json
import sys


class Solution:
    def hasTrailingZeros(self, nums) -> bool:
        return sum(x % 2 == 0 for x in nums) >= 2


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().hasTrailingZeros(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
