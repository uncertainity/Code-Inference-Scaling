import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    seen = set()
    counts = {c: 13 for c in "PKHT"}
    for i in range(0, len(s), 3):
        card = s[i:i + 3]
        if card in seen:
            return "GRESKA\n"
        seen.add(card)
        counts[card[0]] -= 1
    return " ".join(str(counts[c]) for c in "PKHT") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
