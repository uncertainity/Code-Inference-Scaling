import sys


VOWELS = set("aeiou")


def convert(word):
    if word[0].lower() in VOWELS:
        return word + "yay"
    for i, ch in enumerate(word):
        if ch.lower() in VOWELS:
            return word[i:] + word[:i] + "ay"
    return word + "ay"


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    out = []
    for line in data.splitlines():
        out.append(" ".join(convert(w) for w in line.split()))
    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    sys.stdout.write(solve())
