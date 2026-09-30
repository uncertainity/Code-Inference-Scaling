N = int(input())
Q = list(map(int, input().split()))
A = list(map(int, input().split()))
B = list(map(int, input().split()))

INF = 10 ** 18
ans = 0

# 料理Aを作る個数xを固定
for x in range(max(Q) + 1):
    minY = INF # 料理Bを作る個数
    for q, a, b in zip(Q, A, B):
        if x * a > q: # 材料が足らないので不可能
            break
        y = (q - x * a) // b if b != 0 else INF
        minY = min(minY, y)
    else:
        ans = max(ans, x + minY)

print(ans)