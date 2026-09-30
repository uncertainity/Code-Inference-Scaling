
all_numbers = []
def make_number(n):
    all_numbers.append(n)
    for m in range(n%10):
        make_number(10*n + m)

for n in range(1, 10):
    make_number(n)


all_numbers.sort()


print(all_numbers[int(input())-1])