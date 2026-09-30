



def dfs(i,n,t,teams,hate):
    if i == n:
        if len(teams) == t:
            return 1
        else:
            return 0
    if len(teams) > t:
        return 0
    ans = 0
    for j in range(len(teams)):
        if hate[i] & teams[j] != 0:
            continue
        teams[j] ^= 1<<i
        ans += dfs(i+1,n,t,teams,hate)
        teams[j] ^= 1<<i
    
    teams.append(1<<i)
    ans += dfs(i+1,n,t,teams,hate)
    teams.pop()
    return ans


def main():
    n,t,m = map(int,input().split())
    hate = [0 for _ in range(n)]

    for i in range(m):
        a,b = map(int,input().split())
        a -= 1
        b -= 1
        hate[a] ^= 1 << b
        hate[b] ^= 1 << a
    
    ans = 0
    teams = []
    ans = dfs(0,n,t,teams,hate)
    print(ans)



main()
