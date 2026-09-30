N = int(input())
x, *P = map(int, input().split())
if N == 1:
  print(0)
  exit()
Pm = max(P)
print(0 if x > Pm else Pm - x + 1)
