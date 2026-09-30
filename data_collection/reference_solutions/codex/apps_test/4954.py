import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    n, budget, hotels, weeks = vals[:4]
    i = 4
    best = budget + 1
    for _ in range(hotels):
        price = vals[i]
        beds = vals[i + 1:i + 1 + weeks]
        i += 1 + weeks
        if any(b >= n for b in beds):
            best = min(best, price * n)
    return (str(best) if best <= budget else "stay home") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
