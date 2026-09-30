import ast
import sys


class Solution:
    def maximumBeauty(self, nums, k: int) -> int:
        nums.sort()
        ans = left = 0
        for right, x in enumerate(nums):
            while x - nums[left] > 2 * k:
                left += 1
            ans = max(ans, right - left + 1)
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums, k = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return str(Solution().maximumBeauty(nums, k))


if __name__ == "__main__":
    sys.stdout.write(solve())
