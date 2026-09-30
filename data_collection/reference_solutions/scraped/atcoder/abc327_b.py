B = int(input())

for A in range(1, 100):
    if A ** A == B:
        print(A)
        break
else:
    print(-1)