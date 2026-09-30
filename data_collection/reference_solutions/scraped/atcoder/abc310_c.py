import sys
input = sys.stdin.readline

n = int(input())
s = [input().strip() for _ in range(n)]
t = set()

for w in s:
    if w not in t and w[::-1] not in t:
        t.add(w)

print(len(t))