import ast
import sys


class Solution:
    def missingInteger(self, nums) -> int:
        total = nums[0]
        i = 1
        while i < len(nums) and nums[i] == nums[i - 1] + 1:
            total += nums[i]
            i += 1
        seen = set(nums)
        while total in seen:
            total += 1
        return total


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().missingInteger(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
