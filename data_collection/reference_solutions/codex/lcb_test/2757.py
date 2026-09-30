import ast
import sys
from functools import lru_cache


MOD = 10 ** 9 + 7


class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        def upto(num):
            @lru_cache(None)
            def dp(i, total, tight):
                if total > max_sum:
                    return 0
                if i == len(num):
                    return int(total >= min_sum)
                limit = int(num[i]) if tight else 9
                ans = 0
                for d in range(limit + 1):
                    ans += dp(i + 1, total + d, tight and d == limit)
                return ans % MOD
            return dp(0, 0, True)

        lower = str(int(num1) - 1)
        return (upto(num2) - upto(lower)) % MOD


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return str(Solution().count(vals[0], vals[1], vals[2], vals[3]))


if __name__ == "__main__":
    sys.stdout.write(solve())
