l = list(map(int, input().split()))
print("Yes" if all(l[i] <= l[i+1] and (l[i+1] - l[i]) % 25 == 0 for i in range (7)) and l[0] >= 100 and l[7] <= 675 and l[0] % 25 == 0 else "No")



