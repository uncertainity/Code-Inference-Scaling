import sys
from sys import stdin, setrecursionlimit
from math import gcd, lcm, perm, comb, sqrt
import heapq as hq
from types import GeneratorType
def ceil(x): return int(x) if(x == int(x)) else int(x)+1
def ceildiv(x, d): return x//d if(x % d == 0) else x//d+1
MOD = 1_000_000_007
# setrecursionlimit(10**6)
input = lambda: stdin.readline().strip()
######### main code goes here #########

def main():
    N = int(input())
    D = list(map(int, input().split()))
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())

    inf_ = float('inf')
    dp = [inf_] * (K1 + 1)
    dp[0] = 0

    for d in D:
        kmax = min(ceildiv(d, L1), K1)
        b = [0] * (kmax + 1)
        for k in range(kmax + 1):
            rem = d - k * L1
            b[k] = ceildiv(rem, L2) if rem > 0 else 0

        new_dp = [inf_] * (K1 + 1)
        for k in range(kmax + 1):
            bk = b[k]
            nd = new_dp
            for a in range(K1 - k + 1):
                da = dp[a]
                if da == inf_:
                    continue
                v = da + bk
                if v < nd[a + k]:
                    nd[a + k] = v
        dp = new_dp

    ans = inf_
    for a in range(K1 + 1):
        bcnt = dp[a]
        if bcnt <= K2:
            cost = C1 * a + C2 * bcnt
            if cost < ans:
                ans = cost

    print(ans if ans != inf_ else -1)

main()