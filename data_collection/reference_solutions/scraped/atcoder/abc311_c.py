def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC311 C 448 3Q - Find it! 350点
N = ip()
A = [0] + lmp()
i = 1
done = [False] * (N+1)
done[1] = True
while not done[A[i]]:
  i = A[i]
  done[i] = True
last = i
cur = A[i]
ans = [A[i]]
while cur != last:
  cur = A[cur]
  ans.append(cur)
print(len(ans))
print(*ans)
