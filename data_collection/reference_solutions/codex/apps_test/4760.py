import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, k = map(int, data.split())
    removed = [False] * (n + 1)
    count = 0
    for p in range(2, n + 1):
        if removed[p]:
            continue
        for x in range(p, n + 1, p):
            if not removed[x]:
                removed[x] = True
                count += 1
                if count == k:
                    return str(x) + "\n"
    return ""


if __name__ == "__main__":
    sys.stdout.write(solve())
