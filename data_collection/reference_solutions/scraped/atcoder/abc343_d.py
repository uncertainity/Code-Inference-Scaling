import sys
from collections import defaultdict

def main():
  input_data = sys.stdin.read().split()
  N = int(input_data[0])
  T = int(input_data[1])
  ptr = 2
  scores = [0] * N
  kinds = defaultdict(int)
  kinds[0] = N
  ans = 1
  results = []
  
  for _ in range(T):
    A = int(input_data[ptr]) - 1
    B = int(input_data[ptr+1])
    ptr += 2
  
    kinds[scores[A]] -= 1
    if kinds[scores[A]] == 0:
      ans -= 1
    scores[A] += B
    kinds[scores[A]] += 1
    if kinds[scores[A]] == 1:
      ans += 1
        
    results.append(str(ans))
    
  sys.stdout.write("\n".join(results))
  
if __name__ == '__main__':
  main()