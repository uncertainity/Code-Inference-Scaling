import ast
import sys


class Solution:
    def removeAlmostEqualCharacters(self, word: str) -> int:
        ans = 0
        i = 1
        while i < len(word):
            if abs(ord(word[i]) - ord(word[i - 1])) <= 1:
                ans += 1
                i += 2
            else:
                i += 1
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().removeAlmostEqualCharacters(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
