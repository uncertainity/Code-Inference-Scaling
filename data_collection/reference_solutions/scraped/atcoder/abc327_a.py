def b():
    return int(input())

N = b()
S = input()
print("Yes" if "ab" in S or "ba" in S else "No")