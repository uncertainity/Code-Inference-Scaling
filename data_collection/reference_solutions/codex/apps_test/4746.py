import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    cap, n = vals[:2]
    onboard = 0
    p = 2
    for i in range(n):
        left, entered, wait = vals[p:p + 3]
        p += 3
        onboard -= left
        if onboard < 0:
            return "impossible\n"
        onboard += entered
        if onboard > cap:
            return "impossible\n"
        if wait and onboard < cap:
            return "impossible\n"
        if i == n - 1 and (wait or onboard):
            return "impossible\n"
    return "possible\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
