import sys


class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        for k in range(1, 61):
            rem = num1 - k * num2
            if rem >= k and bin(rem).count("1") <= k:
                return k
        return -1


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    num1, num2 = map(int, data.split())
    return str(Solution().makeTheIntegerZero(num1, num2))


if __name__ == "__main__":
    sys.stdout.write(solve())
