from itertools import accumulate
from collections import Counter
N = int(input())
A = list(map(int, input().split()))
A3 = sorted(A)
A2 = []
for i in accumulate(A3):
    A2.append(i)
X = Counter(A)
X2 = sorted(X.keys())
X = list(accumulate(X[k] for k in X2))
X = dict(zip(X2, X))
ans = []
for i in range(N):
  ans.append(A2[-1]-A2[X[A[i]]-1])
print(*(ans))