n = int(input())-1

q = n
c = 0
while q >= 5:
	q,r = divmod(q,5)
	c += 1
if c==0:
	print(n*2)
else:
	kmax = c
	q = n
	r = 0
	s = ""
	for k in range(kmax):
		d = 5**(kmax-k)
		q,r = divmod(q,d)
		s += str(q*2)
		q = r
		if k==kmax-1:
			s += str(q*2)
	print(s)
