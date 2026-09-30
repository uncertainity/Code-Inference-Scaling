N,L,R = map(int,input().split())
A = list(map(int,input().split()))
print(*[a if L<=a<=R else L if a<L else R for a in A])