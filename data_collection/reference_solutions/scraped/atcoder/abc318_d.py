n = int (input())

d = []
for i in range(n-1):
    d.append([0]*(i+1)+list(map(int, input().split())))
if n%2 == 1:
    for i in range(n-1):
        d[i].append(0)
    d.append([0]*(n+1))
    n += 1

def dfs(cn, sc):
    
    global ans
    
    seen[cn] = 1
    
    for i in range(n):
        if seen[i] == -1:
            seen[i] = 1
            sc += d[cn][i]
            if min(seen) == 1:
                ans = max(ans, sc)
            else:
                for nn in range(n):
                    if seen[nn] == -1:
                        dfs(nn, sc)
                        break
            seen[i] = -1                    
            sc -= d[cn][i]

    seen[cn] = -1

ans = 0
seen = [-1]*n
dfs(0, 0)
    
print(ans)