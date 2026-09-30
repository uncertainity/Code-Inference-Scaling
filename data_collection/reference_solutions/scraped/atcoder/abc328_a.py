N, X = map(int, input().split())
S = list(map(int, input().split()))

print(sum(x for x in S if x <= X))