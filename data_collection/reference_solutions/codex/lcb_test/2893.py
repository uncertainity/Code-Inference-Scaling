import ast
import sys


class Solution:
    def maxScore(self, nums, x: int) -> int:
        neg = -10 ** 30
        dp = [neg, neg]
        dp[nums[0] & 1] = nums[0]
        for value in nums[1:]:
            p = value & 1
            best = max(dp[p] + value, dp[1 - p] + value - x)
            dp[p] = max(dp[p], best)
        return max(dp)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums, x = [ast.literal_eval(v) for v in data.splitlines() if v.strip()]
    return str(Solution().maxScore(nums, x))


if __name__ == "__main__":
    sys.stdout.write(solve())
