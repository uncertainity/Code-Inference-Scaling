import ast
import sys
from collections import Counter


class Solution:
    def minimumIndex(self, nums) -> int:
        dom, total = Counter(nums).most_common(1)[0]
        left = 0
        n = len(nums)
        for i, x in enumerate(nums[:-1]):
            if x == dom:
                left += 1
            if left * 2 > i + 1 and (total - left) * 2 > n - i - 1:
                return i
        return -1


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().minimumIndex(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
