import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, s, r = vals[:3]
    damaged = set(vals[3:3 + s])
    reserve = set(vals[3 + s:3 + s + r])
    both = damaged & reserve
    damaged -= both
    reserve -= both
    for team in sorted(list(reserve)):
        if team - 1 in damaged:
            damaged.remove(team - 1)
        elif team + 1 in damaged:
            damaged.remove(team + 1)
    return str(len(damaged)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
