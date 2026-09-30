N, L = (int(x) for x in input().split())
A = [int(x) for x in input().split()]
print(sum(a >= L for a in A))
