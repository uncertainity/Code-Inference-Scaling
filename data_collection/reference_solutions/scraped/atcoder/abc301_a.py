N=input('')
S=str(input(''))

def fight(str):
  
  if str.count("T") > str.count("A"):
    print("T")
  
  elif str.count("T") < str.count("A"):
    print("A")
    
  else:
    if str[-1] == "T":
      print("A")
      #上のstr[-1] == "T"のところでTが文字列として扱われることの留意する
    else:
      print("T")
'''
もし最後が同点ならTとAの勝ち星は(Tの勝ち星)=(Nの勝ち星)=N/2
また同点の場合k-1回目の試合で同点に追いついた選手がいる。
よって後ろの勝負(最終戦で勝った選手)によって最終的な勝者を決めることができる
'''

fight(S)
    
'''

N=input('')
S=input('')

def fight(str):
  
  if str.count("T") > str.count("A"):
    print("T")
  
  elif str.count("T") == str.count("A"):
    str = str[:-1]
    fight(str)
    
  else:
    print("A")
    
再起的に処理を行なっても解けるが問題文を全部使っているわけではないのでスマートではない

'''