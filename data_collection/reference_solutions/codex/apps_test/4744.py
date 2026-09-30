import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n = int(data)
    best = 10 ** 18
    for a in range(1, int(n ** (1 / 3)) + 3):
        if n % a:
            continue
        rem = n // a
        for b in range(1, int(rem ** 0.5) + 2):
            if rem % b == 0:
                c = rem // b
                best = min(best, 2 * (a * b + a * c + b * c))
    return str(best) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
