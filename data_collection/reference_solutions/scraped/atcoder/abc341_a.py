N = int(input())
S = ""
for i in range(2 * N + 1):
    if i % 2 == 1:
        S += "0"
    else:
        S += "1"

print(S)