N, M, P =map(int,input().split())
print(max((int((N - M)/P // 1)+1),0))