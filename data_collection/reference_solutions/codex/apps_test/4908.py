import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    a, b, c = map(int, data.split())
    if a + b == c:
        return f"{a}+{b}={c}\n"
    if a - b == c:
        return f"{a}-{b}={c}\n"
    if a * b == c:
        return f"{a}*{b}={c}\n"
    if a // b == c and a % b == 0:
        return f"{a}/{b}={c}\n"
    if a == b + c:
        return f"{a}={b}+{c}\n"
    if a == b - c:
        return f"{a}={b}-{c}\n"
    if a == b * c:
        return f"{a}={b}*{c}\n"
    return f"{a}={b}/{c}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
