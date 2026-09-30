import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, first = vals[0], vals[1]
    times = vals[2:2 + n]
    order = [times[first]] + sorted(times[:first] + times[first + 1:])
    elapsed = solved = penalty = 0
    for t in order:
        if elapsed + t > 300:
            break
        elapsed += t
        penalty += elapsed
        solved += 1
    return f"{solved} {penalty}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
