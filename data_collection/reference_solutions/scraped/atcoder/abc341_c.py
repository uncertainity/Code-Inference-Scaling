"""
a grid with rows H and coluns W
each cell  is represent by S1 -SH of length W ??
cell is denoted by (i(row from top),j(colums from left))
cell is sea if j ="#"
cell is land if j ="."
the perimeter cells [where i is either 1 or H or where j is 1 or W] is sea

takahashi has landed on  a cell in the grid , he then moves N times onthe grid and his movement is in the form of a string T whose characters represents his movements in left to right order
L meaning a left which is i,j-1
R meaning a right which is i,j+1
U meaning a up which is i-1,j
D meaning a down which is i+1,j

what is known is all cells along his path along with the one he landed on are not sea

needed output is to print the number of cells that could be his current position

Key insights:-
finding the path means the starting cell must be  "." and every move in T should move to a cell that is "." not "#"

complexity:-
the complexity would be O(HxWXN)
"""
H,W,N=map(int,input().split())
T=input()
grid=[]
for i in range(H):
    grid.append(input())

count =0

for i in range(H):
    for j in range(W):
        if  grid[i][j] == ".":
            ci,cj=i,j
            for c in T:
                if c =="L":
                    cj -= 1
                    if grid[ci][cj]!=".":
                        break
                elif c =="R":
                    cj +=1
                    if grid[ci][cj]!=".":
                        break
                elif c == "D":
                    ci +=1
                    if grid[ci][cj]!=".":
                        break
                elif c == "U":
                    ci -=1
                    if grid[ci][cj]!=".":
                        break
                else :
                    print("invalid move")
            else:
                count +=1
print(count)









