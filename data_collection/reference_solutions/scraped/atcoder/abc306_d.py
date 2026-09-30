N = int(input())
X,Y=[],[]
for i in range(N):
	x,y=map(int,input().split())
	X.append(x)
	Y.append(y)
INF = 10**20
dp,ep = 0,-INF # 元気、壊すの順 # 到達不可能の-INF
for i in range(N):
	# 食べない場合
	# 「同じ状態の」直前の最適値を保持
	ndp, nep = dp, ep
	# 食べる場合
	if X[i] == 1: # 毒入りを食べる
		# 元気 -> 毒
		nep = max(nep, dp + Y[i])
	else: # 解毒剤入りを食べる
		# 壊す->元気、元気->元気
		ndp = max(ndp, ep+Y[i], dp+Y[i])
	dp, ep = ndp, nep
print(max(dp, ep))