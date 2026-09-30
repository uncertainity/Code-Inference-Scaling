import sys
input = sys.stdin.readline

N = int(input())

J = []
for j in range(1, 9+1):
    if N%j == 0: J.append(j)

ans = []
for i in range(N+1):
    for j in J:
        if i%(N//j) == 0: 
            ans.append(str(j))
            break
    else: 
        ans.append("-")
print("".join(ans))