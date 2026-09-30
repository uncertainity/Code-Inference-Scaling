import ast
import sys


class Solution:
    def largestPerimeter(self, nums) -> int:
        nums.sort()
        total = sum(nums)
        for i in range(len(nums) - 1, 1, -1):
            if total - nums[i] > nums[i]:
                return total
            total -= nums[i]
        return -1


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().largestPerimeter(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
