import ast
import sys


class Solution:
    def incremovableSubarrayCount(self, nums) -> int:
        n = len(nums)

        def increasing(arr):
            return all(arr[i] < arr[i + 1] for i in range(len(arr) - 1))

        ans = 0
        for left in range(n):
            for right in range(left, n):
                if increasing(nums[:left] + nums[right + 1:]):
                    ans += 1
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().incremovableSubarrayCount(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
