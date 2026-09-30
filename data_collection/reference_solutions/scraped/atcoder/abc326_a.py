X,Y = map(int,input().split())
if (0 < Y - X <= 2) or (0 < X - Y <= 3):
  print("Yes")
else:
  print("No")