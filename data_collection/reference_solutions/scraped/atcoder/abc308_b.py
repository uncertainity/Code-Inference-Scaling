N,M=map(int,input().split())
A=list(map(str,input().split()))
B=list(map(str,input().split()))
S=list(map(int,input().split()))
price=0
for a in A:
    if a in B:
        price+=S[B.index(a)+1]
    else:
        price+=S[0]
print(price)
