import math
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    m, n, t = map(int, data.split())
    cap = m + 1
    if t == 1:
        value = 1
        for i in range(2, n + 1):
            value *= i
            if value > m:
                break
    elif t == 2:
        value = cap if n > 60 else 2 ** n
    elif t == 3:
        value = n ** 4
    elif t == 4:
        value = n ** 3
    elif t == 5:
        value = n ** 2
    elif t == 6:
        value = n * math.log2(n)
    else:
        value = n
    return ("AC" if value <= m else "TLE") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
