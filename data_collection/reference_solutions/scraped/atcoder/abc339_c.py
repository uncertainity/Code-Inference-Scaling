import sys 
data = sys.stdin.read().split()

n = int(data[0])
a_list = list(map(int,data[1:]))
passengers = 0

for a in a_list:
    passengers += a
    if passengers < 0:
        passengers = 0

print(passengers)