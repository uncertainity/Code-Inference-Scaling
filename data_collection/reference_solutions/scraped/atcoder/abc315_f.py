import sys
sys.setrecursionlimit(2*10**7)
#↓codon===============================
import string
Alp_low=list(string.ascii_lowercase)
Alp_up=list(string.ascii_uppercase)
Digit="0123456789"
dij=[[0,1],[1,0],[0,-1],[-1,0]]
def nin():
    return list(map(int,input().split()))
def de(x):
    return [i-1 for i in x]
mod=998244353
def main():
    n,=nin()
    p=[nin() for i in range(n)]
    dp=[[10**36]*30 for i in range(n)]
    for i in range(n):
        if i==0:
            dp[i][0]=0
            continue
        for j in range(30):
            for jj in range(30):
                if j-jj>=0 and i-1-jj>=0:
                    dp[i][j]=min(dp[i][j],dp[i-1-jj][j-jj]+((p[i][0]-p[i-1-jj][0])**2+(p[i][1]-p[i-1-jj][1])**2)**0.5)
    #for i in dp:print(*i)
    for j in range(30):
        if j==0:
            continue
        dp[-1][j]+=2**(j-1)
    print(min(dp[-1]))
    #for i in dp:print(*i)

if __name__=="__main__":
    main()
