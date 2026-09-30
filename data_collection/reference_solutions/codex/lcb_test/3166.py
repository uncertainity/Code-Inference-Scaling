import ast
import sys
from collections import Counter


class Solution:
    def minGroupsForValidAssignment(self, nums) -> int:
        counts = list(Counter(nums).values())
        for size in range(min(counts), 0, -1):
            total = 0
            ok = True
            for c in counts:
                groups = (c + size) // (size + 1)
                if groups * size > c:
                    ok = False
                    break
                total += groups
            if ok:
                return total
        return len(nums)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().minGroupsForValidAssignment(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
