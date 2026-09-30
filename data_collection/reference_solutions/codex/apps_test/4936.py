import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    temps = vals[1:]
    best = min((max(temps[i], temps[i + 2]), i + 1) for i in range(len(temps) - 2))
    return f"{best[1]} {best[0]}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
