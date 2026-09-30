import ast
import json
import sys


class Solution:
    def splitWordsBySeparator(self, words, separator: str):
        ans = []
        for word in words:
            ans.extend(part for part in word.split(separator) if part)
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words, separator = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return json.dumps(Solution().splitWordsBySeparator(words, separator))


if __name__ == "__main__":
    sys.stdout.write(solve())
