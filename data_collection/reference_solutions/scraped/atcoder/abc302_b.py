import sys
H, W = map(int, sys.stdin.readline().split())
S = [sys.stdin.readline().strip() for _ in range(H)]
target = "snuke"
directions = [
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]
def solve():
    for r in range(H):
        for c in range(W):
            if S[r][c] == 's':
                for dr, dc in directions:
                    coords = []
                    valid = True
                    for i in range(5):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < H and 0 <= nc < W and S[nr][nc] == target[i]:
                            coords.append((nr + 1, nc + 1))
                        else:
                            valid = False
                            break
                    if valid:
                        for res in coords:
                            print(f"{res[0]} {res[1]}")
                        return
solve()
