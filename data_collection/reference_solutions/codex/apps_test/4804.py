import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    out = [f"{n}:"]
    for a in range(2, n):
        for b in (a - 1, a):
            if n % (a + b) in (0, a):
                out.append(f"{a},{b}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
