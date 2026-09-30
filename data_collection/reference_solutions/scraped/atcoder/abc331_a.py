ki = input()
a_ki = ki.split(" ")
m0 = int(a_ki[0])
d0 = int(a_ki[1])

ki = input()
a_ki = ki.split(" ")
y = int(a_ki[0])
m = int(a_ki[1])
d = int(a_ki[2])

d += 1
if d > d0:
	d = 1
	m += 1
	if m > m0:
		m = 1
		y += 1
print(f"{y} {m} {d}")
