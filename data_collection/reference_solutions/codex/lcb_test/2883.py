import ast
import sys


class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        powers = set()
        x = 1
        while len(bin(x)) - 2 <= len(s):
            powers.add(bin(x)[2:])
            x *= 5
        n = len(s)
        dp = [10 ** 9] * (n + 1)
        dp[0] = 0
        for i in range(n):
            if dp[i] == 10 ** 9 or s[i] == "0":
                continue
            for j in range(i + 1, n + 1):
                if s[i:j] in powers:
                    dp[j] = min(dp[j], dp[i] + 1)
        return -1 if dp[n] == 10 ** 9 else dp[n]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().minimumBeautifulSubstrings(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
