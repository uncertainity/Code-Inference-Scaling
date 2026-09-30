import ast
import json
import sys


class Solution:
    def checkArray(self, nums, k: int) -> bool:
        n = len(nums)
        diff = [0] * (n + 1)
        active = 0
        for i, x in enumerate(nums):
            active += diff[i]
            cur = x + active
            if cur < 0:
                return False
            if cur:
                if i + k > n:
                    return False
                active -= cur
                diff[i + k] += cur
        return True


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums, k = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return json.dumps(Solution().checkArray(nums, k))


if __name__ == "__main__":
    sys.stdout.write(solve())
