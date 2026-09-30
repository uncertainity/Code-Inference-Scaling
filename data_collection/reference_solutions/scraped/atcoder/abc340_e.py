import sys
class DBIT:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    #内部用 i番目以降にxを加算
    def _add(self, i, x):
        while i <= self.size:
            self.tree[i] += x
            i += i & -i

    #lからrまでにxを加算する
    def add(self, l, r, x):
        self._add(l, x)
        self._add(r + 1, -x)

    #i番目の値を求める
    def get(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    

def debug(*x):print('debug:',*x, file=sys.stderr)
sys.setrecursionlimit(300000)
input = lambda: sys.stdin.readline().rstrip()
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
inf = 2 ** 61 - 1
mod = 998244353
#mod=10**9+7
dy=[-1,1,0,0]
dx=[0,0,-1,1]
#dy=[-1,-1,-1,1,1,1,0,0]
#dx=[-1,0,1,-1,0,1,-1,1]

n,m=mi()
a=li()
b=li()
db=DBIT(2*n+1)
for i in range(n):
    db.add(i+1,i+1,a[i])


for i in range(m):
    bi=b[i]+1
    now1=db.get(bi)
    now2=db.get(bi+n)
    now=now1+now2
    db.add(bi,bi,-now1)
    db.add(bi+n,bi+n,-now2)
    db.add(1,n,now//n)
    db.add(bi+1,bi+now%n,1)
    #print(now1,now2,bi)
    #for i in range(2*n+1):
    #    print(db.get(i),end=" ")

for i in range(1,n+1):
    print(db.get(i)+db.get(i+n),end=" ")
print()