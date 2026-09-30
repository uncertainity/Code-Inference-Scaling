def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC303 D 778 2Q - Shift vs. CapsLock 400点
# あなたのパソコンのキーボードには、a キー・Shift キー・CapsLock キーの 3 種類のキーがあります。
# また、CapsLock キーにはランプが付いています。
# 初め、CapsLock キーのランプは OFF であり、パソコンの画面には空文字列が表示されています。
# あなたは、以下の 3 種類の操作のうち 1 つを選んで実行するということを 0 回以上何度でも行うことができます。
# ・X ミリ秒かけて a キーのみを押す。CapsLock キーのランプが OFF ならば画面の文字列の末尾に a が付け足され、ON ならば A が付け足される。
# ・Y ミリ秒かけて Shift キーと a キーを同時に押す。CapsLock キーのランプが OFF ならば画面の文字列の末尾に A が付け足され、 ON ならば a が付け足される。
# ・Z ミリ秒かけて CapsLock キーを押す。CapsLock キーのランプが OFF ならば ON に、ON ならば OFF に切り替わる。
# A と a からなる文字列 S が与えられます。画面の文字列を S に一致させるのに必要な最短の時間は何ミリ秒かを求めてください。
# ・1 ≤ X, Y, Z ≤ 10^9
# ・1 ≤ |S| ≤ 3×10^5
X, Y, Z = mp()
S = input()
INF = 10**18
dp = [0, INF]
for c in S:
  ndp = [INF, INF]
  if c == 'a':
    ndp[0] = min(dp[0] + X, dp[1] + Z + X)
    ndp[1] = min(dp[0] + Z + Y, dp[1] + Y)
  else:
    ndp[0] = min(dp[0] + Y, dp[1] + Z + Y)
    ndp[1] = min(dp[0] + Z + X, dp[1] + X)
  dp = ndp
print(min(dp))