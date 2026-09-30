import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    code = data.strip()
    lengths = []
    i = 0
    while i < len(code):
        j = i + 1
        while j < len(code) and code[j].islower():
            j += 1
        lengths.append(j - i)
        i = j
    pos = ans = 0
    for length in lengths:
        pad = (-pos) % 4
        ans += pad
        pos += pad + length
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
