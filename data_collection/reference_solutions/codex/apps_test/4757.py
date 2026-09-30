import sys


def solve(data=None):
    if data is None:
        data = sys.stdin.read()
    lines = data.splitlines()
    n = int(lines[0])
    songs = [set() for _ in range(n + 1)]
    new_song = 0
    for line in lines[2:]:
        nums = list(map(int, line.split()))
        villagers = nums[1:]
        if 1 in villagers:
            new_song += 1
            for v in villagers:
                songs[v].add(new_song)
        else:
            union = set()
            for v in villagers:
                union |= songs[v]
            for v in villagers:
                songs[v] = set(union)
    return "".join(str(i) + "\n" for i in range(1, n + 1) if len(songs[i]) == new_song)


if __name__ == "__main__":
    sys.stdout.write(solve())
