import sys
from collections import defaultdict


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    n = int(lines[0])
    visits = defaultdict(list)
    for line in lines[1:1 + n]:
        country, year = line.split()
        visits[country].append(int(year))
    for years in visits.values():
        years.sort()
    q = int(lines[1 + n])
    out = []
    for line in lines[2 + n:2 + n + q]:
        country, k = line.split()
        out.append(str(visits[country][int(k) - 1]))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
