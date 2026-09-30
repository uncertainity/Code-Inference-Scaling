from itertools import product

p = [[[*input()] for _ in range(4)] for _ in range(3)]

for k in range(3):
  for t in [0, -1]:
    while set(p[k][t]) == {'.'}:
      p[k].pop(t)
  
    h = len(p[k])
    while {p[k][i][t] for i in range(h)} == {'.'}:
      for i in range(h):
        p[k][i].pop(t)

def rot(l, r):
  return rot([*zip(*l[::-1])], r-1) if r > 0 else l

for i, j, r in product(product(range(4), repeat= 3), repeat= 3):
  field = [[0] * 4 for _ in range(4)]

  for k in range(3):
    l = rot(p[k], r[k])
    h = len(l)
    w = len(l[0])

    for ii in range(h):
      for jj in range(w):
        if i[k]+h-1 < 4 and j[k]+w-1 < 4:
          field[i[k]+ii][j[k]+jj] += l[ii][jj] == '#'

  if field == [[1] * 4 for _ in range(4)]:
    print("Yes")
    exit()

print("No")