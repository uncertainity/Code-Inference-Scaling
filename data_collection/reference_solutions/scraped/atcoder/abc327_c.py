a_yx = []
for y in range(9):
	ki = input()
	a_ki = ki.split(" ")
	a_x = [int(v) for v in a_ki]
	a_yx.append(a_x)

f = 0
while True:
	for y in range(9):
		st_x = set(a_yx[y])
		if not len(st_x)==9:
			f = 1
			break
	if f==1:
		break
	
	for x in range(9):
		st_y = set()
		for y in range(9):
			st_y.add(a_yx[y][x])
		if not len(st_y)==9:
			f = 1
			break
	if f==1:
		break
	
	for y in range(3):
		for x in range(3):
			st_b = set()
			for y1 in range(3):
				for x1 in range(3):
					by = y*3+y1
					bx = x*3+x1
					st_b.add(a_yx[by][bx])
			if not len(st_b)==9:
				f = 1
				break
		if f==1:
			break
	break

res = "No"
if f==0:
	res = "Yes"
print(res)
