import ast
import json
import sys


class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        ones = s.count("1")
        return "1" * (ones - 1) + "0" * (len(s) - ones) + "1"


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().maximumOddBinaryNumber(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
