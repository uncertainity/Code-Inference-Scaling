import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    g, s, c = map(int, data.split())
    power = 3 * g + 2 * s + c
    victory = "Province" if power >= 8 else "Duchy" if power >= 5 else "Estate" if power >= 2 else ""
    treasure = "Gold" if power >= 6 else "Silver" if power >= 3 else "Copper"
    return (victory + " or " + treasure if victory else treasure) + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
