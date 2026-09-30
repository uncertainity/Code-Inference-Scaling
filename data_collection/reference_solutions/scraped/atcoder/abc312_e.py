def nxt(i, j, k):
  if i < 0 or i >= M or j < 0 or j >= M or k < 0 or k >= M:
    return -1
  return C[i][j][k]
  

def adj(c, i, j, k):
  for di, dj, dk in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
    ni, nj, nk = i + di, j + dj, k + dk
    nc = nxt(ni, nj, nk)
    if nc >= 0:
      A[c].append(nc)
      A[nc].append(c)


def mark(c, x1, x2, xs, y1, y2, ys, z1, z2, zs):
  for i in range(x1, x2, xs):
    for j in range(y1, y2, ys):
      for k in range(z1, z2, zs):
        C[i][j][k] = c
        adj(c, i, j, k)
        

N = int(input())
M = 100
C = [[[-1] * M for _ in range(M)] for _ in range(M)]
A = [[] for _ in range(N)]
for c in range(N):
  x1, y1, z1, x2, y2, z2 = list(map(int, input().split()))
  mark(c, x1, x2, 1, y1, y2, 1, z1, z2, max(1, z2 - z1 - 1))
  mark(c, x1, x2, 1, y1, y2, max(1, y2 - y1 - 1), z1, z2, 1)
  mark(c, x1, x2, max(1, x2 - x1 - 1), y1, y2, 1, z1, z2, 1)
ans = "\n".join(map(str, (len(set(A[i]) - set([-1, i])) for i in range(N))))
print(ans)
