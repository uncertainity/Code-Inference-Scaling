n = int(input())

ki = input()
a_ki = ki.split(" ")
a_lk = [int(v) for v in a_ki]

dt_lk = {}
for i in range(n):
	dt_lk[a_lk[i]] = i+1

mb = -1
a_m = []
for i in range(n):
	m = dt_lk[mb]
	a_m.append(str(m))
	mb = m
print(" ".join(a_m))
