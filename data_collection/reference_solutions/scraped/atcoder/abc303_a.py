N = int(input())
S = input()
T = input()
print("Yes" if all(S[i] == T[i] or (S[i] in ("l", "1") and T[i] in ("l", "1")) or (S[i] in ("o", "0") and T[i] in ("o", "0")) for i in range (N)) else "No")