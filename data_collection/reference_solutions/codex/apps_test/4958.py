import itertools
import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    vals = list(map(int, data.split()))
    boxes, h1, h2 = vals[:6], vals[6], vals[7]
    for group in itertools.combinations(boxes, 3):
        if sum(group) == h1:
            first = sorted(group, reverse=True)
            rest = boxes[:]
            for x in group:
                rest.remove(x)
            second = sorted(rest, reverse=True)
            return " ".join(map(str, first + second)) + "\n"
    raise ValueError("no tower")


if __name__ == "__main__":
    sys.stdout.write(solve())
