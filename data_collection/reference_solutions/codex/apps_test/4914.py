import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    parts = data.split()
    s = parts[1]
    patterns = [("Adrian", "ABC"), ("Bruno", "BABC"), ("Goran", "CCAABB")]
    scores = []
    for name, pat in patterns:
        scores.append((sum(ch == pat[i % len(pat)] for i, ch in enumerate(s)), name))
    best = max(x for x, _ in scores)
    return str(best) + "\n" + "\n".join(name for x, name in scores if x == best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
