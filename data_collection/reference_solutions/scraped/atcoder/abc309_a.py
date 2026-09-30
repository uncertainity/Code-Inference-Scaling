A, B = map(int, input().split())

if B - A == 1 and (A - 1) // 3 == (B - 1) // 3:
    print("Yes")
else:
    print("No")