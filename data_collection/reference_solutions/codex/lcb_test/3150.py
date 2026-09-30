import ast
import json
import sys


class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        ans = ""
        left = ones = 0
        for right, ch in enumerate(s):
            ones += ch == "1"
            while ones > k:
                ones -= s[left] == "1"
                left += 1
            while left <= right and s[left] == "0":
                left += 1
            if ones == k:
                cur = s[left:right + 1]
                if not ans or (len(cur), cur) < (len(ans), ans):
                    ans = cur
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s, k = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return json.dumps(Solution().shortestBeautifulSubstring(s, k))


if __name__ == "__main__":
    sys.stdout.write(solve())
