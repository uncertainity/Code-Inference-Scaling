import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    days = list(map(int, data.split()[1:]))
    cleanups = 0
    group = []
    for day in days:
        if sum(day - old for old in group) >= 20:
            cleanups += 1
            group = []
        group.append(day)
    return str(cleanups + 1) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
