import ast
import sys


class Solution:
    def countTestedDevices(self, batteryPercentages):
        tested = 0
        for battery in batteryPercentages:
            if battery > tested:
                tested += 1
        return tested


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return str(Solution().countTestedDevices(ast.literal_eval(data.strip())))


if __name__ == "__main__":
    sys.stdout.write(solve())
