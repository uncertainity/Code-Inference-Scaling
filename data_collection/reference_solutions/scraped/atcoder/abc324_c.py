N,T = input().split()
N = int(N)
A = []

for i in range(N):
  S = input()

  if len(T) == len(S):
    if T == S:
      A.append(i+1)
    else:
      flg = 0
      for j in range(len(S)):
        if S[j] != T[j]:
          flg += 1
        if flg > 1:
          break
      else:
        A.append(i+1)
        
  elif len(T)-len(S) == 1:
    flg = 0
    for j in range(len(S)+1):
      if j-flg >= len(S):
        continue
      if S[j-flg] != T[j]:
        flg += 1
      if flg > 1:
        break
    else:
      A.append(i+1)
  elif len(S)-len(T) == 1:
    flg = 0
    for j in range(len(S)):
      if j - flg >= len(T):
        continue
      if S[j] != T[j-flg]:
        flg += 1
      if flg > 1:
        break
    else:
      A.append(i+1)
print(len(A))
for i in range(len(A)):
  print(A[i],end = " ")