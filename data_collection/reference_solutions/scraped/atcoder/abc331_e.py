# ABC 331-E

import sys
input = sys.stdin.readline


def main():
    N, M, L = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    NG = [tuple(map(int, input().split())) for _ in range(L)]

    counter = [dict() for _ in range(N)]
    for i in range(L):
        c, d = NG[i]
        c -= 1; d -= 1
        val = B[d]
        if val in counter[c]:
            counter[c][val] += 1
        else:
            counter[c][val] = 1
    
    B.sort(reverse=True)

    ans_max = -1
    for i in range(N):
        idx = 0
        while idx < M:
            val = B[idx]
            if val in counter[i]:
                counter[i][val] -= 1
                if counter[i][val] == 0:
                    counter[i].pop(val)
            else:
                ans_max = max(ans_max, A[i] + val)
                break
            idx += 1
    
    print(ans_max)


if __name__ == "__main__":
    main()