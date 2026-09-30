
n=int(input())
m = (n - 1).bit_length()
print(m)
A=[[] for _ in range(m)]
for i in range(m):
    a=[]
    for j in range(n):
        jj=j//(2**(i))%2
        A[i].append(jj)
        if jj:
            a.append(j+1)
    print(len(a),*a)
#print(A)
s=input()
for i in range(n):
    for j in range(m):
        if A[j][i]!=int(s[j]):
            break
    else:
        print(i+1)
        break
