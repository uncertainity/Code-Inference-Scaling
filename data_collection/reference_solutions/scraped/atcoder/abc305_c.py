H, W = map(int, input().split())
S = [input() for _ in range(H)]
tate = set()
yoko = set()

for i in range(H):
  for j in range(W):
    if S[i][j] == "#":
      tate.add(i)
      yoko.add(j)

for t in tate:
  for y in yoko:
    if S[t][y] == ".":
      print(t+1, y+1)
      exit()