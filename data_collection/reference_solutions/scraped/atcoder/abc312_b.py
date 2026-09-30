N, M = map(int, input().split())
L = [input() for _ in range(N)]

for i in range(N - 8):
    for j in range(M - 8):
        for k in range(3):
            if L[i + k][j:j + 4] != "###." or L[i + 6 + k][j + 5:j + 5 + 4] != ".###":
                break
        else:
            if L[i + 3][j:j + 4] == "...." and L[i + 5][j + 5:j + 5 + 4] == "....":
                print(i + 1, j + 1)