import sys
input = sys.stdin.readline

n, m, h, k = map(int, input().split())
s = input().rstrip()
item = set()
x = y = 0

for _ in range(m):
    X, Y = map(int, input().split())
    item.add((X,Y))

for w in s:
    if w == "R":
        x += 1
    elif w == "L":
        x -= 1
    elif w == "U":
        y += 1
    else:
        y -= 1

    h -= 1
    if h < 0:
        print("No")
        break

    if (x, y) in item and h < k:
        h = k
        item.remove((x, y))
else:
    print("Yes")