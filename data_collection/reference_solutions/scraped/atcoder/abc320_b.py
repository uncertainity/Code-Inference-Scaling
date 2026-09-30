s = input()

l, r = 0, len(s) - 1

def is_palindrome(st):
    return st == st[::-1]

longest_palindrom = 0
for i in range(0, len(s)):
    for j in range(i, len(s) + 1):
        if is_palindrome(s[i:j]):
            longest_palindrom = max(j - i, longest_palindrom)

print(longest_palindrom)
