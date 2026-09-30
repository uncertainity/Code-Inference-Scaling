import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    s, v1, v2 = map(int, data.split())
    best = None
    for a in range(s // v1, -1, -1):
        rem = s - a * v1
        if rem % v2 == 0:
            best = (a, rem // v2)
            break
    return "Impossible\n" if best is None else f"{best[0]} {best[1]}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
