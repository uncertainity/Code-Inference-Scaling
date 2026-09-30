N = int(input())
grid = [input() for _ in range(N)]
row = [0]*N
col = [0]*N

for i in range(N):
  for j in range(N):
    if grid[i][j] == "o":
      row[i] += 1
      col[j] += 1

ans = 0
for i in range(N):
  for j in range(N):
    if grid[i][j] == "o":
      ans += (row[i]-1)*(col[j]-1)

print(ans)