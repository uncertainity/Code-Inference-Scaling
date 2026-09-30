n = int(input())

for d1 in range(n+1):
	for d2 in range(n+1):
		for d3 in range(n+1):
			sm = d1+d2+d3
			if sm > n:
				break
			print(f"{d1} {d2} {d3}")
