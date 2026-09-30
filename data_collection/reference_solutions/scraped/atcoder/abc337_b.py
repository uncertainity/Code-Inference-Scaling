s = input()
ls = len(s)

s1b = ""
t = ""
for i in range(ls):
	s1 = s[i]
	if not s1==s1b:
		t += s1
	s1b = s1

res = "No"
if len(t)==1:
	if t=="A" or t=="B" or t=="C":
		res = "Yes"
elif len(t)==2:
	if t=="AB" or t=="BC" or t=="AC":
		res = "Yes"
elif len(t)==3:
	if t=="ABC":
		res = "Yes"
print(res)
