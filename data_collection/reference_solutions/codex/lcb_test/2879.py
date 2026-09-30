import ast
import sys


class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        divisors = [[] for _ in range(n + 1)]
        for length in range(2, n + 1):
            for d in range(1, length):
                if length % d == 0:
                    divisors[length].append(d)

        cost = [[10 ** 9] * n for _ in range(n)]
        for left in range(n):
            for right in range(left + 1, n):
                length = right - left + 1
                best = 10 ** 9
                for d in divisors[length]:
                    changes = 0
                    for offset in range(d):
                        group = [s[left + i] for i in range(offset, length, d)]
                        changes += sum(group[i] != group[~i] for i in range(len(group) // 2))
                    best = min(best, changes)
                cost[left][right] = best

        dp = [[10 ** 9] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for used in range(k):
            for start in range(n):
                if dp[start][used] >= 10 ** 9:
                    continue
                for end in range(start + 1, n):
                    dp[end + 1][used + 1] = min(dp[end + 1][used + 1],
                                                dp[start][used] + cost[start][end])
        return dp[n][k]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s, k = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return str(Solution().minimumChanges(s, k))


if __name__ == "__main__":
    sys.stdout.write(solve())
