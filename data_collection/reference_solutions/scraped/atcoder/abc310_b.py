N, M = map(int, input().split())
P, C = [], []
F= []
for _ in range(N):
  PCF = list(map(int, input().split()))
  P.append(PCF[0])
  C.append(PCF[1])
  F.append(set(PCF[2:]))

for i in range(N):
  for j in range(N):
    ok1 = ok2 = ok3 = False
    if i == j:
      continue
    if P[i] >= P[j]:
      ok1 = True
    if F[i] <= F[j]:
      ok2 = True
    if (P[i] > P[j]) or (F[i] != F[j]):
      ok3 = True

    if ok1 and ok2 and ok3:
      print("Yes")
      exit()
    

print("No")
    