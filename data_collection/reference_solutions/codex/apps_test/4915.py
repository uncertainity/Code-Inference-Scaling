import sys
from collections import defaultdict


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    wrong = defaultdict(int)
    solved = set()
    count = penalty = 0
    for line in data.splitlines():
        if line == "-1":
            break
        minute, problem, result = line.split()
        if problem in solved:
            continue
        if result == "right":
            solved.add(problem)
            count += 1
            penalty += int(minute) + wrong[problem] * 20
        else:
            wrong[problem] += 1
    return f"{count} {penalty}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
