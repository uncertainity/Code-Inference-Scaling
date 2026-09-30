import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    i = 0
    restaurants = int(lines[0])
    i = 1
    for _ in range(restaurants):
        n = int(lines[i])
        i += 1
        restaurant = lines[i]
        i += 1
        menu = set(lines[i:i + n])
        i += n
        if "pea soup" in menu and "pancakes" in menu:
            return restaurant + "\n"
    return "Anywhere is fine I guess\n"


if __name__ == "__main__":
    sys.stdout.write(solve())
