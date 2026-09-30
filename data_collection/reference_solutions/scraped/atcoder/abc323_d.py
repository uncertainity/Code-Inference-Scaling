N = int(input())
slime = {}
for i in range(N):
    own_slime = list(map(int, input().split()))  
    slime[own_slime[0]] = own_slime[1]

# 1 & 2. 辞書のキー（サイズ）を取り出し、小さい順にソートする
sorted_sizes = sorted(slime.keys())

for size in sorted_sizes:
    current_size = size
    
    # 2匹以上いる限り、連鎖的に合成を繰り返す
    while slime.get(current_size, 0) >= 2:
        num = slime[current_size]
        
        # 合成して新しくできる大きいスライムの数
        new_slime_count = num // 2
        # 合成できずにそのサイズに残るスライムの数 (3. 計算の修正)
        leftover = num % 2
        
        # 現在のサイズの数を余りだけにする
        slime[current_size] = leftover
        
        # 2倍のサイズに移動し、新しくできたスライムを足す
        current_size *= 2
        slime[current_size] = slime.get(current_size, 0) + new_slime_count

total = 0
for size, num in slime.items():
    total += num

# 4. num ではなく total を出力する
print(total)