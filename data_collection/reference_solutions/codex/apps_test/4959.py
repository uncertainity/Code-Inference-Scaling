import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    e, f, c = map(int, data.split())
    bottles = e + f
    ans = 0
    while bottles >= c:
        new = bottles // c
        ans += new
        bottles = new + bottles % c
    return str(ans) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
