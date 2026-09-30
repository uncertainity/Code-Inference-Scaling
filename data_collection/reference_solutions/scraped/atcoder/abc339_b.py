def disp(a_yx,h):
	for y in range(h):
		print("".join(a_yx[y]))
	print()


ki = input()
a_ki = ki.split(" ")
h = int(a_ki[0])
w = int(a_ki[1])
n = int(a_ki[2])

a_yx = []
for y in range(h):
	a_yx.append(["."]*w)

y = 0
x = 0
d = 1
a_d = [[0,1],[-1,0],[0,-1],[1,0]]
for c in range(n):
	v = a_yx[y][x]
	if v==".":
		a_yx[y][x] = "#"
		d = (d-1)%4
	else:
		a_yx[y][x] = "."
		d = (d+1)%4
	
	y += a_d[d][0]
	if y==-1:
		y = h-1
	elif y==h:
		y = 0
	x += a_d[d][1]
	if x==-1:
		x = w-1
	elif x==w:
		x = 0

disp(a_yx,h)
