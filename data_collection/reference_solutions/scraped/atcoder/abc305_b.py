p, q = input().split()
dist_list = [3, 1, 4, 1, 5, 9]
alp_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
if alp_list.index(p) < alp_list.index(q):
  dist = dist_list[alp_list.index(p):alp_list.index(q)]
else:
  dist = dist_list[alp_list.index(q):alp_list.index(p)]

print(sum(dist))