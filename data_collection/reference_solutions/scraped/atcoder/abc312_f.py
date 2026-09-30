import sys
input = sys.stdin.readline

n, m = map(int, input().split())
t0 = []
t1 = []
t2 = []
for _ in range(n):
    t, x = map(int, input().split())
    if t == 0: t0.append(x)
    if t == 1: t1.append(x)
    if t == 2: t2.append(x)
t0.sort(reverse=True)
t1.sort(reverse=True)
t2.sort(reverse=True)
d0, d1, d2 = len(t0), len(t1), len(t2)
pf0 = [0] * (d0 + 1)
for i in range(d0):
    pf0[i + 1] = pf0[i] + t0[i]
pf12 = [0] * (m + 1)
ptr1 = 0
ptr2 = 0
rem_opens = 0
curr_sum = 0

for i in range(1, m + 1):
    if rem_opens > 0 and ptr1 < d1:
        curr_sum += t1[ptr1]
        ptr1 += 1
        rem_opens -= 1
    elif ptr2 < d2:
        rem_opens += t2[ptr2]
        ptr2 += 1
    pf12[i] = curr_sum
ans = 0
for i in range(min(d0, m) + 1):
    ans = max(ans, pf0[i] + pf12[m - i])
print(ans)
