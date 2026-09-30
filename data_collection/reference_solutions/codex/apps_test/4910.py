import sys
from collections import Counter


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words = data.split()[1:]
    cnt = Counter(words)
    best = min(cnt.values())
    return "\n".join(sorted(w for w, c in cnt.items() if c == best)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
