ki = input()
a_ki = ki.split(" ")
n = int(a_ki[0])
s = int(a_ki[1])
k = int(a_ki[2])

sm = 0
for i in range(n):
	ki = input()
	a_ki = ki.split(" ")
	p1 = int(a_ki[0])
	m1 = int(a_ki[1])
	sm += p1*m1

if sm < s:
	sm += k
print(sm)
