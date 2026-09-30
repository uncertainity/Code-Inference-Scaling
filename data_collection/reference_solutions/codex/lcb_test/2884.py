import ast
import sys


class Solution:
    def longestValidSubstring(self, word: str, forbidden) -> int:
        blocked = set(forbidden)
        right = len(word) - 1
        best = 0
        for left in range(len(word) - 1, -1, -1):
            for end in range(left, min(len(word), left + 10, right + 1)):
                if word[left:end + 1] in blocked:
                    right = end - 1
                    break
            best = max(best, right - left + 1)
        return best


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    word, forbidden = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return str(Solution().longestValidSubstring(word, forbidden))


if __name__ == "__main__":
    sys.stdout.write(solve())
