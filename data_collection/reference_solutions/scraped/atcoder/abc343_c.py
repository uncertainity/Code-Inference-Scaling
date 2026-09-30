def judge_palindrome(n):
  #これからnの値を変えていくのでnbに保存
  nb=n

  digit=1
  while (n>9):
    digit+=1
    n//=10

  #nを保存用nbで充足
  #逆順数字reversed_nを用意
  n=nb
  reversed_nb=0

  for i in range(digit):
    reversed_nb = reversed_nb*10 + n%10
    n//=10
  if nb==reversed_nb:
    return True
  return False


N=int(input())
x=1
save=1
while (x**3<=N):
  a=x**3
  if judge_palindrome(a):
    save=a
  x+=1
print(save)