N = int(input())
S = input()

exist_a, exist_b, exist_c = False, False, False

for i in range(N):
  if S[i] == 'A': exist_a = True
  if S[i] == 'B': exist_b = True
  if S[i] == 'C': exist_c = True
  if exist_a and exist_b and exist_c:
    print(i + 1)
    break
