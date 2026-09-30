n, m = map(int, input().split())
S = input()
T = input()
from collections import deque

def solve():
    q = deque()
    s = []
    last_chr = []
    for i in range(n):
        q.append(S[i])
    while q:
        x = q.popleft()
        s.append(x)
        if x != "*":
            last_chr.append(len(s) - 1)
        if len(s) >= m and len(last_chr) > 0 and len(s) - m <= last_chr[-1]:
            for j in range(m):
                if s[-1-j] != "*" and s[-1-j] != T[-1-j]:
                    break
            else:
                for _ in range(m):
                    y = s.pop()
                    if y != "*":
                        last_chr.pop()
                    q.appendleft("*")
    for i in range(n):
        if s[i] != "*":
            return False
    return True

ans = solve()
print("Yes" if ans else "No")