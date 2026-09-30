import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words = data.split()[1:]
    seen = set()
    prev = ""
    for i, word in enumerate(words):
        if word in seen or (prev and word[0] != prev[-1]):
            return f"Player {i % 2 + 1} lost\n"
        seen.add(word)
        prev = word
    return "Fair Game\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
