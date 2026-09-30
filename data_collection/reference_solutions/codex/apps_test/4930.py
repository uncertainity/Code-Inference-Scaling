import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vowels = set("aeiou")
    out = []
    i = 0
    while i < len(data):
        out.append(data[i])
        if data[i] in vowels:
            i += 3
        else:
            i += 1
    return "".join(out)


if __name__ == "__main__":
    sys.stdout.write(solve())
