import string

n = int(input())
s = input()
q = int(input())
cd = [list(input().split()) for _ in range(q)]

base = string.ascii_lowercase
alpha = base
for c, d in cd:
    alpha = alpha.replace(c, d)
ans = "".join([alpha[base.index(tar)] for tar in s])
print(ans)
