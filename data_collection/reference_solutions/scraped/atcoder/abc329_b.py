N = int(input())
A = list(map(int, input().split()))

mx = max(A)

second_max = max(x for x in A if x != mx)

print(second_max)