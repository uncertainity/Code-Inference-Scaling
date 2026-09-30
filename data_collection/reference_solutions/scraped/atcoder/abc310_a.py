# Source: https://usaco.guide/general/io

n, o, d = map(int, input().split())
p = input().split(" ")
for i in range(len(p)):
    p[i] = int(p[i])
m = min(p)
f = int(0)
f = d + m
if f < o:
    print(f)
else:
    print(o)