import sys
from itertools import permutations


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n_s, s = data.split()
    n = int(n_s)
    counts = {ch: s.count(ch) for ch in "ABC"}
    doubled = s + s
    pref = {ch: [0] * (2 * n + 1) for ch in "ABC"}
    for i, ch in enumerate(doubled):
        for team in "ABC":
            pref[team][i + 1] = pref[team][i] + (ch == team)

    def have(team, left, length):
        return pref[team][left + length] - pref[team][left]

    best = 0
    for order in permutations("ABC"):
        for start in range(n):
            pos = start
            score = 0
            for team in order:
                length = counts[team]
                score += have(team, pos, length)
                pos += length
            best = max(best, score)
    return str(n - best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
