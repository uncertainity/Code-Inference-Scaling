import sys


class Solution:
    def differenceOfSums(self, n: int, m: int) -> int:
        return sum(i if i % m else -i for i in range(1, n + 1))


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, m = map(int, data.split())
    return str(Solution().differenceOfSums(n, m))


if __name__ == "__main__":
    sys.stdout.write(solve())
