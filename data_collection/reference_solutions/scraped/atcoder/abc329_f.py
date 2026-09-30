N, Q = map(int, input().split())
C = list(map(int, input().split()))

# 箱の中身を移動させるのではなく、箱自体を交換する
s = [set([c]) for c in C]
for _ in range(Q):
    a, b = map(lambda x: int(x) - 1, input().split())
    if len(s[a]) < len(s[b]):
        s[b] |= s[a]
        s[a] = set()
    else:
        s[a] |= s[b]
        s[b] = set()
        s[a], s[b] = s[b], s[a]
    print(len(s[b]))