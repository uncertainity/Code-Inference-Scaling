N = int(input())
S = str(input())
s = set()
num = 1
if N == 1:
    print(1)
else:
    s.add((S[0],1))
    for i in range(1,N):
        if S[i] == S[i-1]:
            num += 1
            s.add((S[i],num))
        else:
            s.add((S[i],1))
            num = 1
    print(len(s))