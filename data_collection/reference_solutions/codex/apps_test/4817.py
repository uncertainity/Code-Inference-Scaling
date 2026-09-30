import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a = list(data.strip())
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return "0\n"
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = sorted(a[i + 1:])
    return "".join(a) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
