N = int(input())
S = input()

zero = 0 # 現在位置で終わるすべての部分文字列のうち、NAND値0であるものの個数
one =  0 # 現在位置で終わるすべての部分文字列のうち、NAND値1であるものの個数
ans = 0

# NAND値の性質：左が0なら必ず1、左が1なら反転
for s in S:
    old_zero, old_one = zero, one
    
    if s == "0":
        # sを部分文字列の一文字目として使う場合、新しくNAND値0ができる
        zero = 1
        
        # 以前の部分文字列のNAND値に関わらず、必ずNAND値1になる。以前zero個あったNAND値0も、以前one個あったもNAND値1も全てNAND値1になる
        one = old_zero + old_one
    
    elif s == "1":
        # 以前の部分文字列のNAND値1だったものはNAND値0になる
        zero = old_one
        
        # 以前の部分文字列のNAND値0だったものはNAND値1になる。sを部分文字列の一文字目として使う場合、新しくNAND値1ができるので+1
        one = old_zero + 1
    
    ans += one

print(ans)