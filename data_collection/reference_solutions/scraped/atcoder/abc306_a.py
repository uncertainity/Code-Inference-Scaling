N=int(input())
S=input()

lit=""

for i in range(N):
  lit+=S[i]+S[i]

print(lit)