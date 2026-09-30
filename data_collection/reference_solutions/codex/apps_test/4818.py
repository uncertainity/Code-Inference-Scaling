import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    tasks = sorted(vals[2:2 + vals[0]])
    intervals = sorted(vals[2 + vals[0]:])
    i = ans = 0
    for length in intervals:
        if i < len(tasks) and tasks[i] <= length:
            ans += 1
            i += 1
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
