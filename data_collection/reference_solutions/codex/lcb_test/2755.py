import ast
import sys


class Solution:
    def minExtraChar(self, s: str, dictionary) -> int:
        words = set(dictionary)
        n = len(s)
        dp = [0] + [10 ** 9] * n
        for i in range(n):
            dp[i + 1] = min(dp[i + 1], dp[i] + 1)
            for j in range(i + 1, n + 1):
                if s[i:j] in words:
                    dp[j] = min(dp[j], dp[i])
        return dp[n]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = [line for line in data.splitlines() if line.strip()]
    return str(Solution().minExtraChar(ast.literal_eval(lines[0]), ast.literal_eval(lines[1])))


if __name__ == "__main__":
    sys.stdout.write(solve())
