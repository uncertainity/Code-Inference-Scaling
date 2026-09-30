import ast
import itertools
import json
import sys


class Solution:
    def minimumString(self, a: str, b: str, c: str) -> str:
        def merge(x, y):
            if y in x:
                return x
            best = 0
            for k in range(1, min(len(x), len(y)) + 1):
                if x[-k:] == y[:k]:
                    best = k
            return x + y[best:]

        ans = None
        for parts in itertools.permutations([a, b, c]):
            cur = merge(merge(parts[0], parts[1]), parts[2])
            if ans is None or (len(cur), cur) < (len(ans), ans):
                ans = cur
        return ans


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, c = [ast.literal_eval(x) for x in data.splitlines() if x.strip()]
    return json.dumps(Solution().minimumString(a, b, c))


if __name__ == "__main__":
    sys.stdout.write(solve())
