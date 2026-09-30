a_g1 = ["AB","BC","CD","DE","AE"]

a_g = []
for i in range(2):
	s = input()
	if s[0] > s[1]:
		s = s[1]+s[0]
	g = 0
	if s in a_g1:
		g = 1
	a_g.append(g)

res = "No"
if a_g[0]==a_g[1]:
	res = "Yes"
print(res)
