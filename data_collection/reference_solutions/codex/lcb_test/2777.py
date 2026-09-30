import ast
import json
import sys
from collections import Counter


class Solution:
    def distinctDifferenceArray(self, nums):
        right = Counter(nums)
        left = set()
        ans = []
        for x in nums:
            left.add(x)
            right[x] -= 1
            if right[x] == 0:
                del right[x]
            ans.append(len(left) - len(right))
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().distinctDifferenceArray(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
