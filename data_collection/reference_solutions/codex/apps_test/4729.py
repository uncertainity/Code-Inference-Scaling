import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    word, hidden = data.split()
    i = 0
    letters = set(word)
    for ch in hidden:
        if i < len(word) and ch == word[i]:
            i += 1
        elif ch in set(word[i + 1:]):
            return "FAIL\n"
    return ("PASS" if i == len(word) else "FAIL") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
