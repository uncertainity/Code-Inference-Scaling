import ast
import json
import sys


class Solution:
    def sortVowels(self, s: str) -> str:
        vowels = set("aeiouAEIOU")
        pool = sorted(ch for ch in s if ch in vowels)
        it = iter(pool)
        return "".join(next(it) if ch in vowels else ch for ch in s)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().sortVowels(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
