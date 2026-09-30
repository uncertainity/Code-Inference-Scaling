import sys


MOD = 10 ** 9 + 7


class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        powers = []
        base = 1
        while base ** x <= n:
            powers.append(base ** x)
            base += 1
        dp = [0] * (n + 1)
        dp[0] = 1
        for value in powers:
            for total in range(n, value - 1, -1):
                dp[total] = (dp[total] + dp[total - value]) % MOD
        return dp[n]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, x = map(int, data.split())
    return str(Solution().numberOfWays(n, x))


if __name__ == "__main__":
    sys.stdout.write(solve())
