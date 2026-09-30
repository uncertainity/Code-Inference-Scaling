import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    nums = list(map(int, data.split()[1:]))
    missing = [str(x) for x in range(1, nums[-1] + 1) if x not in set(nums)]
    return "\n".join(missing) + ("\n" if missing else "good job\n")


if __name__ == "__main__":
    sys.stdout.write(solve())
