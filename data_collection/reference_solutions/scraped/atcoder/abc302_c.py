import sys
import itertools
input = sys.stdin.readline
def solve():
    n, m = map(int, input().split())
    s=[]
    for i in range(n):
        ss = input().strip()
        s.append(ss)
    
    p=itertools.permutations(range(n),n)
    for ilist in p:
        for i in range(n-1):
            ss1=s[ilist[i]]
            ss2=s[ilist[i+1]]
            check=0
            for j in range(m):
                if ss1[j]!=ss2[j]:
                    check+=1
            if check!=1:
                break
        else:
            print("Yes")
            return
    print("No")


    
    return

if __name__ == '__main__':
    solve()