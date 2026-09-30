import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    words = data.split()
    count = sum("ae" in word for word in words)
    return ("dae ae ju traeligt va" if count * 100 >= 40 * len(words) else "haer talar vi rikssvenska") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
