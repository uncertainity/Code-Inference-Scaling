import sys
data = sys.stdin.read().split()

n = int(data[0])
ans_list = []
for time in range(24):
    ans = 0
    for i in range(1,2*n+1,2):
        x = int(data[i+1])
        if 9 <= (x + time)%24 <= 17:
            ans += int(data[i])
    ans_list.append(ans)

print(max(ans_list))