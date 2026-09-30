import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    mode, s = data.split(maxsplit=1)
    s = s.rstrip("\n")
    if mode == "E":
        out = []
        i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            out.append(s[i] + str(j - i))
            i = j
        return "".join(out) + "\n"
    out = []
    for i in range(0, len(s), 2):
        out.append(s[i] * int(s[i + 1]))
    return "".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
