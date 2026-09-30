s = input()
ls = len(s)

a_c = []
for i in range(26):
	s1 = chr(ord("a")+i)
	a_c.append([0,s1])

for i in range(ls):
	s1 = s[i]
	j = ord(s1)-ord("a")
	a_c[j][0] += 1

a_c.sort(key=lambda x:(-x[0],x[1]))
print(a_c[0][1])
