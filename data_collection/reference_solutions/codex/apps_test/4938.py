import sys
from collections import deque


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    limit = int(lines[0])
    q = deque(lines[1].strip())
    diff = served = 0
    while q:
        gender = q[0]
        val = 1 if gender == "M" else -1
        if abs(diff + val) <= limit:
            q.popleft()
            diff += val
            served += 1
        elif len(q) >= 2:
            gender = q[1]
            val = 1 if gender == "M" else -1
            if abs(diff + val) <= limit:
                q.remove(gender)
                diff += val
                served += 1
            else:
                break
        else:
            break
    return str(served) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
