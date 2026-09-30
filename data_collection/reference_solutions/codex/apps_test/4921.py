import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    seen = set()
    out_lines = []
    for line in data.splitlines():
        out = []
        for word in line.split():
            key = word.lower()
            if key in seen:
                out.append(".")
            else:
                seen.add(key)
                out.append(word)
        out_lines.append(" ".join(out))
    return "\n".join(out_lines) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
