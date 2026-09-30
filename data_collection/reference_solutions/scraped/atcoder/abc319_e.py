import sys
input = sys.stdin.readline

# N = int(input())
N, X, Y = map(int, input().split())
bus = [list(map(int, input().split())) for _ in range(N-1)]

lcm = 840
DP = [-1]*(lcm+1)

ans = []
for _ in range(int(input())):
    S = int(input())
    if DP[S%lcm] != -1: ans.append(S+DP[S%lcm]); continue
    ret = S + X
    for p, t in bus:
        ret += -ret%p + t
    ret += Y
    DP[S%lcm] = ret-S
    ans.append(ret)
print("\n".join(map(str, ans)))