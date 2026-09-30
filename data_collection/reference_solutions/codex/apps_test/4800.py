import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    n, k, target, current = map(float, data.split())
    need = (target * n - current * k) / (n - k)
    if need < 0 or need > 100:
        return "impossible\n"
    if abs(need - round(need, 2)) < 1e-9:
        return f"{need:.2f}\n"
    return f"{need:.7f}\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
