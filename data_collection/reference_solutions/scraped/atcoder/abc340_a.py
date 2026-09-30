ki = input()
a_ki = ki.split(" ")
a = int(a_ki[0])
b = int(a_ki[1])
d = int(a_ki[2])

a_n = []
for n in range(a,b+1,d):
	a_n.append(str(n))

print(" ".join(a_n))
