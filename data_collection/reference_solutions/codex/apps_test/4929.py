import sys


def toggles(s):
    for i, ch in enumerate(s):
        if ch.isalpha():
            yield s[:i] + ch.swapcase() + s[i + 1:]


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    password, attempt = data.split()
    ok = password.lower() == attempt.lower()
    ok = ok or any(password + d == attempt or d + password == attempt for d in "0123456789")
    ok = ok or attempt in set(toggles(password))
    return ("Yes" if ok else "No") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
