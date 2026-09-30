N = int(input())
l = list(map(int, input().split()))
s = 0
ll = []
for i in range(7*N):
    s += l[i]
    if i%7 == 6:
        ll += [s]
        s = 0
print(*ll)