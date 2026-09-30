sn = input()
ln = len(sn)
n = int(sn)

c = 0
d = 2
for i in range(n):
	if n%d==0:
		c += 1
		d *= 2
	else:
		break
print(c)
