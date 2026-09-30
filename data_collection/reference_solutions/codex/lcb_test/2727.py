import ast
import sys


class Solution:
    def countSeniors(self, details):
        return sum(int(x[11:13]) > 60 for x in details)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    details = ast.literal_eval(data.strip())
    return str(Solution().countSeniors(details))


if __name__ == "__main__":
    sys.stdout.write(solve())
