st_r = set()
for c1 in range(1,13):
	r1 = int("1"*c1)
	for c2 in range(c1,13):
		r2 = int("1"*c2)
		for c3 in range(c2,13):
			r3 = int("1"*c3)
			sm = r1+r2+r3
			st_r.add(sm)
a_r = list(st_r)
a_r.sort()

n = int(input())
print(a_r[n-1])
