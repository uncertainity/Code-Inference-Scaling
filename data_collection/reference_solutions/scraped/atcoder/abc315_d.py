#ただの趣味レーション問題

h, w = map(int, input().split())

g = [list(input()) for _ in range(h)]

hh = [{} for _ in range(h)]
ww = [{} for _ in range(w)]

for i in range(h):
    for j in range(w):
        c = g[i][j]

        if c in hh[i]:
            hh[i][c] += 1
        else:
            hh[i][c] = 1

        if c in ww[j]:
            ww[j][c] += 1
        else:
            ww[j][c] = 1

deleted_h = [False] * h
deleted_w = [False] * w

hcnt = [w] * h
wcnt = [h] * w

while True:
    erase_h = []
    erase_w = []

    # 今の盤面で消せる行を探す
    for i in range(h):
        if deleted_h[i]:
            continue
        if hcnt[i] >= 2 and len(hh[i]) == 1:
            erase_h.append(i)

    # 今の盤面で消せる列を探す
    for j in range(w):
        if deleted_w[j]:
            continue
        if wcnt[j] >= 2 and len(ww[j]) == 1:
            erase_w.append(j)

    if not erase_h and not erase_w:
        break

    # 行を削除する
    for i in erase_h:
        deleted_h[i] = True
        for j in range(w):
            if deleted_w[j]:
                continue

            c = g[i][j]
            ww[j][c] -= 1
            if ww[j][c] == 0:
                del ww[j][c]
            wcnt[j] -= 1

    # 列を削除する
    for j in erase_w:
        deleted_w[j] = True
        for i in range(h):
            if deleted_h[i]:
                continue

            c = g[i][j]
            hh[i][c] -= 1
            if hh[i][c] == 0:
                del hh[i][c]
            hcnt[i] -= 1

ans = 0
for i in range(h):
    if deleted_h[i]:
        continue
    ans += hcnt[i]

print(ans)