import sys
sys.setrecursionlimit(10**6)
from collections import *
N=int(input())
num=deque()
for i in range(1,N**2):
    num.append(i)
ans=[[0 for _ in range(N)]for _ in range(N)]
now_direction="R"
direction={"R":"D","D":"L","L":"U","U":"R"}

def move(i,j,nd):
    global ans
    if len(num)==0:
        return 
    if 0<=i<=N-1 and 0<=j<=N-1:
        if nd=="R":
            if ans[i][j]==0:
                ans[i][j]=num.popleft()
                if j==N-1 or ans[i][j+1]!=0:
                    nd=direction["R"]
                    move(i+1,j,nd)
                move(i,j+1,nd)
        if nd=="D":
            if ans[i][j]==0:
                ans[i][j]=num.popleft()
                if i==N-1 or ans[i+1][j]!=0:
                    nd=direction["D"]
                    move(i,j-1,nd)
                move(i+1,j,nd)
        if nd=="L":
            if ans[i][j]==0:
                ans[i][j]=num.popleft()
                if j==0 or ans[i][j-1]!=0:
                    nd=direction["L"]
                    move(i-1,j,nd)
                move(i,j-1,nd)
        if nd=="U":
            if ans[i][j]==0:
                ans[i][j]=num.popleft()
                if j==N-1 or ans[i-1][j]!=0:
                    nd=direction["U"]
                    move(i,j+1,nd)
                move(i-1,j,nd)

move(0,0,"R")
ans[(N-1)//2][(N-1)//2]="T"
for i in ans:
    print(*i)