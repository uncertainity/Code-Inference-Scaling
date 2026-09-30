N = int(input())

# 円環を切り開く
chords = [-1] * (2 * N)
for i in range(N):
    a, b = map(lambda x: int(x) - 1, input().split())
    a, b = min(a, b), max(a, b)
    chords[a] = i # 点aと点bを両端とする弦番号iを記録
    chords[b] = i

stack = []
seen = [False] * N
for chord in chords:
    if not seen[chord]: # 弦chordの始点
        seen[chord] = True
        stack.append(chord)
    else: # 弦chordの終点
        if stack[-1] != chord:
            print("Yes")
            break
        stack.pop()
else:
    print("No")