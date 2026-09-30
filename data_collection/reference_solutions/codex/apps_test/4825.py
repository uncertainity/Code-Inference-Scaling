import sys


MAP = {
    "a": "@", "b": "8", "c": "(", "d": "|)", "e": "3", "f": "#", "g": "6",
    "h": "[-]", "i": "|", "j": "_|", "k": "|<", "l": "1", "m": "[]\\/[]",
    "n": "[]\\[]", "o": "0", "p": "|D", "q": "(,)", "r": "|Z", "s": "$",
    "t": "']['", "u": "|_|", "v": "\\/", "w": "\\/\\/", "x": "}{", "y": "`/",
    "z": "2",
}


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    return "".join(MAP.get(ch.lower(), ch) for ch in data)


if __name__ == "__main__":
    sys.stdout.write(solve())
