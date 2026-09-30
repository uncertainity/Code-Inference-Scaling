import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words = data.split()[1:]
    ans = sum("pink" in w.lower() or "rose" in w.lower() for w in words)
    return (str(ans) if ans else "I must watch Star Wars with my daughter") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
