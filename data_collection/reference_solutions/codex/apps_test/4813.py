import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    word, guesses = data.split()
    missed = 0
    remaining = set(word)
    for ch in guesses:
        if ch in remaining:
            remaining.remove(ch)
            if not remaining:
                return "WIN\n"
        else:
            missed += 1
            if missed == 10:
                return "LOSE\n"
    return "WIN\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
