class Csum_2d:
    def __init__(self,board):
        h = len(board)
        w = len(board[0])
        csum = [[0 for _ in range(w+1)] for _ in range(h+1)]

        for y in range(h):
            for x in range(w):
                csum[y+1][x+1] = csum[y+1][x] + csum[y][x+1] - csum[y][x] + board[y][x]

        self.csum = csum

    def query(self,y1,x1,y2,x2):
        #0-indexedの半開区間
        return self.csum[y2][x2] - self.csum[y1][x2] - self.csum[y2][x1] + self.csum[y1][x1]


def solve(y,x,n,csum):
    ans = 0
    total = csum.query(0,0,n,n)
    ans += (y//n) * (x//n) * total
    right = csum.query(0,0,n,x%n)
    ans += right * (y//n)
    down = csum.query(0,0,y%n,n)
    ans += down * (x//n)
    migishita = csum.query(0,0,y%n,x%n)
    ans += migishita
    return ans

def solve2(a,b,c,d,n,csum):
    ans = 0
    ans += solve(c+1,d+1,n,csum)
    ans -= solve(a,d+1,n,csum)
    ans -= solve(c+1,b,n,csum)
    ans += solve(a,b,n,csum)
    return ans

def main2():
    n = int(input())
    board = []
    for _ in range(n):
        board.append(list(map(int,input().split())))
    csum = Csum_2d(board)
    y,x = map(int,input().split())
    print(solve(y,x,n,csum))

#main2()

def main():
    n,q = map(int,input().split())
    board = []
    for _ in range(n):
        line = input()
        temp = []
        for j in range(n):
            temp.append(1 if line[j] == "B" else 0)
        board.append(temp)
    csum = Csum_2d(board)
    ans = []
    for _ in range(q):
        a,b,c,d = map(int,input().split())
        ans.append(solve2(a,b,c,d,n,csum))
    

    for line in ans:
        print(line)



main()

