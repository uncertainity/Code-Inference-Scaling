import ast
import sys


class Solution:
    def maxStrength(self, nums):
        if len(nums) == 1:
            return nums[0]
        positives = [x for x in nums if x > 0]
        negatives = sorted(x for x in nums if x < 0)
        if len(negatives) % 2:
            negatives.pop()
        chosen = positives + negatives
        if not chosen:
            return 0 if 0 in nums else max(nums)
        ans = 1
        for x in chosen:
            ans *= x
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().maxStrength(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
