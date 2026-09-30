q = int(input())

a_q = []
for i in range(q):
	a_q.append(input())

a_a = []
for i in range(q):
	ki = a_q[i]
	a_ki = ki.split(" ")
	c = int(a_ki[0])
	p = int(a_ki[1])
	if c==1:
		a_a.append(p)
	else:
		print(a_a[-p])
