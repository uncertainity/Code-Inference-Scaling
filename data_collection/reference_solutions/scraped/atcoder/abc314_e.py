#期待値DP
#
#操作回数の期待値は
#現在地から、それぞれの遷移先について(遷移先の値 * そこに遷移する確率)を計算して
#その総和に+1したものとなる。
#
#コストの期待値は
#現在地から、それぞれの遷移先について(遷移先の値 * そこに遷移する確率)を計算して
#その総和に現在地のコストを加算したものとなる。
#
#すると、以下の方針によるメモ化再帰で解ける
#
#memo[x] = 現在地がxである場合に、以降に必要なコストの期待値
#memo[0]の場合、既にゴール済なので追加コストは必要ないからmemo[0]=0となり、
#これがベースケースとなる。
#
#あるルーレットをまわしたときに獲得ポイントが0となる場合があるため、その分はコストを
#増加させる。
#つまり、コスト100でルーレットの値が(0,20,10)だった場合、
#memo[x] = cost[x] + 1/3(memo[x] + memo[x-20] + memo[x-10])となり両辺にmemo[x]が
#登場するため、
# ================================================================================
# memo[x]-1/3(memo[x]) = cost[x] + 1/3(memo[x-20]) + 1/3(memo[x-10])
# 2/3(memo[x]) = cost[x] + 1/3(memo[x-20]) + 1/3(memo[x-10]) →両辺に3/2を掛け算して、
# memo[x] = 3/2(cost[x]) + 1/2(memo[x-20]) + 1/2(memo[x-10])
# ================================================================================
#という調整が必要になる。具体的には100 * 3/2をしてコストを150にし、各遷移先への遷移確率を調整する。
#(https://qiita.com/hyouchun/items/b4e09230f4c0daf81ac0を参照)

import sys
sys.setrecursionlimit(10**6)
n,m = list(map(int,input().split()))

r1 = [] #コスト
r2 = [] #各ルーレットの目

for i in range(n):
    tmp = list(map(int,input().split()))
    c = tmp[0]
    p = tmp[1]
    s = tmp[2:]

    #ルーレットに0がなければそのままr1とr2に入れる
    if s.count(0) == 0:
        r1.append(c)
        r2.append(s)

    #ルーレットに0があった場合は0を取り除きコストと遷移確率の調整をした上でr1とr2に入れる
    else:
        ss = []
        for j in s:
            if j > 0:
                ss.append(j)
        r1.append(c*(p/len(ss)))
        r2.append(ss)

#メモ化再帰でベースケースの設定
#memo[x] = x起点の場合の追加コストの期待値とする
memo = {0:0}

def rec(x):
    if x in memo:
        return memo[x]

    cost = 10**10
    
    #現在の値がxの時に、全てのルーレットを回してみて一番コストの期待値の
    #小さいものを採用する
    for i in range(n):
        tmpcost = r1[i]

        for j in range(len(r2[i])):
            nex = max(x-r2[i][j],0)
            tmpcost += rec(nex)/len(r2[i])
        
        cost = min(cost,tmpcost)

    memo[x] = cost
    return memo[x]

print(rec(m))
