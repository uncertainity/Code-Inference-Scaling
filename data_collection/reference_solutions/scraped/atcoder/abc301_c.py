from collections import Counter

S = input()
T = input()

cs = Counter(S)
ct = Counter(T)

ok = set("atcoder")

# atcoder以外は個数が完全一致している必要がある
for c in set(cs.keys()) | set(ct.keys()):
    if c == '@' or c in ok:
        continue
    if cs[c] != ct[c]:
        print("No")
        exit()

need_s = 0
need_t = 0

for c in ok:
    if cs[c] < ct[c]:
        need_s += ct[c] - cs[c]
    elif cs[c] > ct[c]:
        need_t += cs[c] - ct[c]

if need_s <= cs['@'] and need_t <= ct['@']:
    print("Yes")
else:
    print("No")
    