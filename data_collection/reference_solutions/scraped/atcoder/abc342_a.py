s=input()
ans=0
for i in range(1,len(s)):
  if s[0]==s[1]:
    if s[0]!=s[i]:
      ans+=(i+1)
      
if s[0]!=s[1]:
    if s[0]==s[2]:
      ans+=2
    if s[0]!=s[2]:
      ans+=1

print(ans)