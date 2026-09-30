from collections import defaultdict, deque

N, M = map(int, input().split())
S = input()
C = list(map(int, input().split()))

d = defaultdict(lambda: deque())
for s, c in zip(S, C):
    d[c].append(s)

for v in d.values():
    v.appendleft(v.pop())

ans = []
for c in C:
    ans.append(d[c].popleft())
print("".join(ans))