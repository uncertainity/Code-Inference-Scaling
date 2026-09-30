import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(float, data.split()))
    have = vals[:3]
    ratio = vals[3:]
    scale = min(h / r for h, r in zip(have, ratio))
    return " ".join(f"{h - scale * r:.6f}" for h, r in zip(have, ratio)) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
