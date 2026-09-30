import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s = data.strip()
    out = []
    i = 0
    beats = {"R": "S", "B": "K", "L": "H"}
    while i < len(s):
        chunk = s[i:i + 3]
        if len(chunk) == 3 and set(chunk) == set("RBL"):
            out.append("C")
            i += 3
        else:
            out.append(beats[s[i]])
            i += 1
    return "".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
