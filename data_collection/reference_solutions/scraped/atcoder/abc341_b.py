import sys
def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    A = list(map(int, input_data[1:N+1]))
    ST = []
    idx = N + 1
    for _ in range(N - 1):
        s = int(input_data[idx])
        t = int(input_data[idx+1])
        ST.append((s, t))
        idx += 2
    for i in range(N - 1):
        s, t = ST[i]
        num = A[i] // s
        A[i+1] += num * t
    print(A[N-1])
solve()
