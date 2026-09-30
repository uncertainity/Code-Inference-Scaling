n, m = map(int, input().split())
a = list(map(int, input().split()))

li = [0] * (n+1)
ans = 1
for i in range(m):
    li[a[i]] += 1
    if li[ans] < li[a[i]]:
        ans = a[i]
    elif li[ans] == li[a[i]] and ans > a[i]:
        ans = a[i]
    print(ans)