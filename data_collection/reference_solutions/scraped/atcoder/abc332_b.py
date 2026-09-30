ki = input()
a_ki = ki.split(" ")
k = int(a_ki[0])
yg = int(a_ki[1])
ym = int(a_ki[2])

g = 0
m = 0
for k1 in range(k):
	if g==yg:
		g = 0
	elif m==0:
		m = ym
	else:
		rg = yg-g
		if rg >= m:
			g,m = g+m,0
		else:
			g,m = yg,m-rg

print(f"{g} {m}")
