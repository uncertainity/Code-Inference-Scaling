import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, t = vals[0], vals[1]
    a = vals[2:2 + n]
    if t == 1:
        seen = set()
        for x in a:
            if 7777 - x in seen:
                return "Yes\n"
            seen.add(x)
        return "No\n"
    if t == 2:
        return ("Unique" if len(set(a)) == n else "Contains duplicate") + "\n"
    if t == 3:
        for x, c in Counter(a).items():
            if c > n // 2:
                return str(x) + "\n"
        return "-1\n"
    a.sort()
    if t == 4:
        if n % 2:
            return str(a[n // 2]) + "\n"
        return f"{a[n // 2 - 1]} {a[n // 2]}\n"
    return " ".join(map(str, [x for x in a if 100 <= x <= 999])) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
