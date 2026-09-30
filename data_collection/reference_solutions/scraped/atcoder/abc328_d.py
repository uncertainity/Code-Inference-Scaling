from collections import deque


DQ = deque([])
S = input()
for s in S:
    if s == "C" and len(DQ) >= 2 and DQ[-1] == "B" and DQ[-2] == "A":
        DQ.pop()
        DQ.pop()
    else:
        DQ.append(s)
print("".join(DQ))