n = int(input())

ki = input()
a_ki = ki.split(" ")
a_md = [int(v) for v in a_ki]

c = 0
for i in range(n):
	m = i+1
	d = a_md[i]
	c1 = 0
	if m < 10:
		if d >= m:
			c1 += 1
		if d >= m*10+m:
			c1 += 1
	elif m > 10:
		sm = str(m)
		ml = int(sm[0])
		mr = int(sm[1])
		if ml==mr:
			if d >= ml:
				c1 += 1
			if d >= m:
				c1 += 1
	c += c1
print(c)
