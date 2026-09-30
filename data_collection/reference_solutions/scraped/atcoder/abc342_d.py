from collections import defaultdict, Counter

N = int(input())
A = list(map(int, input().split()))

# 素因数分解
def prime_factorize(x):
    res = []
    while x % 2 == 0:
        x //= 2
        res.append(2)
    f = 3
    while f * f <= x:
        while x % f == 0:
            x //= f
            res.append(f)
        else:
            f += 2
    if x != 1:
        res.append(x)
    return res

d = defaultdict(int)
ans = 0
for i, a in enumerate(A):
    if a == 0:
        ans += i
        d[0] += 1
        continue
    
    res = prime_factorize(a)
    cnt = Counter(res)
    tmp = 1 # aを割り切る最大の平方数を調べる
    for k, v in cnt.items():
        if v % 2 == 1: # 素因数の指数が奇数であるものを残す（平方因子を取り除く）
            tmp *= k
    
    ans += d[0] + d[tmp]
    d[tmp] += 1

print(ans)