import ast
import json
import sys
from collections import Counter, defaultdict


class Solution:
    def lastNonEmptyString(self, s: str) -> str:
        total = Counter(s)
        target = max(total.values())
        seen = defaultdict(int)
        ans = []
        for ch in s:
            seen[ch] += 1
            if total[ch] == target and seen[ch] == target:
                ans.append(ch)
        return "".join(ans)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().lastNonEmptyString(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
