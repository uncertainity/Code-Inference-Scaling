import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    vals = sorted(map(int, lines[0].split()))
    mp = dict(zip("ABC", vals))
    return " ".join(str(mp[ch]) for ch in lines[1].strip()) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
