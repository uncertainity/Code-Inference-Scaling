def ip():return int(input())
def mp():return map(int, input().split())
def lmp():return list(map(int, input().split()))
# ABC319 D 631 2Q - Minimum Width 400点
# 高橋くんは、N 個の単語からなる文章をウィンドウに表示させようとしています。
# すべての単語の縦幅は等しく、i 番目 (1≤i≤N) の単語の横幅は Li です。
# 文章は、横幅 1 の空白を単語の区切りとしてウィンドウに表示されます。
# より厳密には、高橋くんが横幅 W のウィンドウに文章を表示しているとき、次の条件が成り立っています。
# ・文章はいくつかの行に分かれている。
# ・1 番目の単語は一番上の行の先頭に表示されている。
# ・i 番目 (2≤i≤N) の単語は、i-1 番目の単語の次に間隔を 1 だけ開けて表示されているか、
# i-1 番目の単語が含まれる行の下の行の先頭に表示されているかの一方である。
# それ以外の場所に表示されていることはない。
# ・それぞれの行の横幅は W を超えない。
# ここで、行の横幅とは最も左にある単語の左端から最も右にある単語の右端までの距離を指す。
# 高橋くんが文章をウィンドウに表示したとき、文章が M 行に収まりました。
# ウィンドウの横幅としてありえる最小の値を求めてください。
# ・1 ≤ M ≤ N ≤ 2×10^5
# ・1 ≤ Li ≤ 10^9 (1 ≤ i ≤ N)
N, M = mp()
L = lmp()
def judge(x):
  i = 0
  row = 0
  while i < N:
    if L[i] > x:
      return False
    sum_ = L[i]
    row += 1
    i += 1
    while i < N and sum_ + 1 + L[i] <= x:
      sum_ += 1 + L[i] 
      i += 1
  return row <= M
ng, ok = 0, sum(L) + N - 1
while ok - ng > 1:
  mi = (ok + ng) // 2
  if judge(mi):
    ok = mi
  else:
    ng = mi
print(ok)
