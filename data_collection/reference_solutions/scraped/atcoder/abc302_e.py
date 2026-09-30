N, Q = map(int, input().split())

G = [set() for _ in range(N + 1)]
cnt = N

for _ in range(Q):
    com, *u, v = map(int, input().split())
    if com == 1:
        u = u[0]
        G[u].add(v)
        G[v].add(u)
        if len(G[u]) == 1:
            cnt -= 1
        if len(G[v]) == 1:
            cnt -= 1
    elif com == 2:
        if G[v]:
            for to in G[v]:
                G[to].remove(v)
                if len(G[to]) == 0:
                    cnt += 1
            G[v] = set()
            cnt += 1
    print(cnt)