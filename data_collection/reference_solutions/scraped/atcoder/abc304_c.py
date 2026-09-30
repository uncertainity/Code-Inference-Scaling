N, D = (int(x) for x in input().split())
coords = [tuple(int(x) for x in input().split()) for _ in range(N)]

graph = [[] for _ in range(N)]
for i in range(N):
    ax, ay = coords[i]
    for j in range(N):
        bx, by = coords[j]
        if (ax - bx) ** 2 + (ay - by) ** 2 <= D ** 2:
            graph[i].append(j)

result = [False] * N
result[0] = True
stack = [0]
while stack:
    u = stack.pop()
    for v in graph[u]:
        if result[v]:
            continue
        result[v] = True
        stack.append(v)

for r in result:
    if r:
        print("Yes")
    else:
        print("No")
