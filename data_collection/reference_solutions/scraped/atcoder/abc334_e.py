##### Union-Find #####
from collections import defaultdict

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1 for i in range(n)] #各頂点の親番号(自身が根なら-1)を管理
        self.size = [1]*n #各頂点が属する根付き木の頂点数を管理
        self.min_node=[i for i in range(n)] #各頂点が属する根付き木の頂点の最小値
	
	# xを含む根付き木の根番号を返す
    def root(self, x):
        if self.parents[x] == -1:
            return x
        else:
            self.parents[x] = self.root(self.parents[x]) #経路圧縮
            return self.parents[x]
	
	#xとyが同じグループに属すか判定
    def isSame(self, x, y):
        if self.root(x)==self.root(y):
            return True
        else:
            return False
        
	#xを含む根付き木とyを含む根付き木を合併
    def unite(self, x, y):
        x = self.root(x)
        y = self.root(y)
        if x==y:
            return
        #Union by Size(小さい方を大きい方に合併)
        if self.size[x] < self.size[y]:
            x, y = y, x

        self.parents[y] = x
        self.size[x] += self.size[y]

        #min_nodeの更新
        self.min_node[x]=min(self.min_node[x],self.min_node[y])
        
	#xが属する根付き木の要素数を返す
    def Size(self, x):
        return self.size[self.root(x)]
    
    #xが属す根付き木に属する要素をリストで返す
    def members(self, x):
        return [i for i in range(self.n) if self.root(i) == self.root(x)]
        
	#すべての根の要素をリストで返す
    def roots(self):
        return [i for i, x in enumerate(self.parents) if x == -1]
    
    #根付き木の数を返す (N回出力するときは注意: unionする度に1減らせば良い)
    def group_count(self):
        return len(self.roots())
    
    #xを含む根付き木の中での頂点番号の最小値
    def get_min_node(self, x):
        return self.min_node[self.root(x)]
    
	#{根番号:[その根付き木に含まれる要素のリスト],...}のdefaultdictを返す
    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.root(member)].append(member)
        return group_members

    #all_group_membersの結果を文字列で返す
    def __str__(self):
	    return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items()) 


H,W=map(int,input().split())
m=998244353
s=[]
cnt=0
for i in range(H):
    S=input()
    for j in range(W):
        if S[j]==".":
            cnt+=1
    s.append(S)

def idx(i,j):
    return i*W+j

uf=UnionFind(H*W)

for i in range(H):
    for j in range(W):
        if s[i][j]==".":
            continue
        for i1,j1 in [[i+1,j],[i-1,j],[i,j+1],[i,j-1]]:
            if not (0<=i1<H and 0<=j1<W):
                continue
            if s[i1][j1]==".":
                continue
            uf.unite(idx(i,j),idx(i1,j1))

base=uf.group_count()-cnt

bunsi=0
for i in range(H):
    for j in range(W):
        if s[i][j]==".":
            se=set()
            for i1,j1 in [[i+1,j],[i-1,j],[i,j+1],[i,j-1]]:
                if not (0<=i1<H and 0<=j1<W):
                    continue
                if s[i1][j1]==".":
                    continue
                rt=uf.root(idx(i1,j1))
                se.add(rt)

            bunsi+=base-(len(se)-1)

d=pow(cnt,-1,m)
print(bunsi*d%m)