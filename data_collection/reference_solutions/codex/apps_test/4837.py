import sys


WIN = {("S", "P"), ("P", "R"), ("R", "S")}


def score(a, b):
    return 1 if a == b else 2 if (a, b) in WIN else 0


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    rounds = int(lines[0])
    mine = lines[1]
    friends = lines[3:3 + int(lines[2])]
    actual = sum(score(mine[i], f[i]) for f in friends for i in range(rounds))
    best = 0
    for i in range(rounds):
        best += max(sum(score(ch, f[i]) for f in friends) for ch in "RPS")
    return f"{actual}\n{best}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
