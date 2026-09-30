n = int(input())

pt = 0
pa = 0
for i in range(n):
	ki = input()
	a_ki = ki.split(" ")
	pt += int(a_ki[0])
	pa += int(a_ki[1])

if pt > pa:
	res = "Takahashi"
elif pt < pa:
	res = "Aoki"
else:
	res = "Draw"
print(res)
