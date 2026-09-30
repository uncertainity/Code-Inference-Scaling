import ast
import json
import sys
from collections import deque


class Solution:
    def finalString(self, s: str) -> str:
        q = deque()
        rev = False
        for ch in s:
            if ch == "i":
                rev = not rev
            elif rev:
                q.appendleft(ch)
            else:
                q.append(ch)
        if rev:
            q.reverse()
        return "".join(q)


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return json.dumps(Solution().finalString(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
