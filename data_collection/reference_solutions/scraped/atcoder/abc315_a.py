S = input()
ans = ''
for x in S:
  if x not in ['a','i','u','e','o']:
    ans += x
print(ans)