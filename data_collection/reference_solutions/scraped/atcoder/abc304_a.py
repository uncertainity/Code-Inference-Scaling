N = int(input())
l = []
ll = []
for i in range (N):
    a, b = input().split()
    l += [a]
    ll += [int(b)]
a = ll.index(min(ll))
print(*(l[a:] + l[0:a]))