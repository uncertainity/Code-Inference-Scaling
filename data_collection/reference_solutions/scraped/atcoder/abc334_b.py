a,m,l,r = map(int,input().split())

l -= a
r -= a

if l < 0:
    t = -(l//m)
    add = (t+1)*m

    l += add
    r += add

rcnt = r//m
lcnt = (l-1)//m
print(rcnt-lcnt)