import ast
import sys


class Solution:
    def minimizeConcatenatedLength(self, words):
        dp = {(words[0][0], words[0][-1]): len(words[0])}
        for w in words[1:]:
            ndp = {}
            for (first, last), cost in dp.items():
                a = (first, w[-1])
                b = (w[0], last)
                ndp[a] = min(ndp.get(a, 10 ** 9), cost + len(w) - (last == w[0]))
                ndp[b] = min(ndp.get(b, 10 ** 9), cost + len(w) - (w[-1] == first))
            dp = ndp
        return min(dp.values())


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().minimizeConcatenatedLength(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
