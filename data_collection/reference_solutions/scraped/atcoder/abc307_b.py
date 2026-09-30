n = int(input())
vec = []
for i in range(n):
    vec.append(input())

boole = False

for i in range(n):
    for j in range(n):
        if vec[i]==vec[j]:
            continue
        p = vec[i]+vec[j]
        if p == p[::-1]:
            boole = True

if boole:
    print("Yes")
else:
    print("No")